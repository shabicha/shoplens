# VGG16Similarity.py
# Compare cosine similarity + rank
# VGG16 method to extract image features
import numpy as np
from numpy import linalg as LA
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import h5py
from PIL import Image
import requests
from io import BytesIO
from scipy import spatial


class VGGNet:
    def __init__(self):
        # weights: 'imagenet'
        # pooling: 'max' or 'avg'
        # input_shape: (width, height, 3), width and height should >= 48
        self.input_shape = (224, 224, 3)
        # weights pre-trained on the ImageNet dataset
        self.weight = 'imagenet'
        self.pooling = 'max'
        self.model = VGG16(
            weights=self.weight, 
            input_shape=(self.input_shape[0], self.input_shape[1], self.input_shape[2]), 
            pooling=self.pooling, 
            include_top=False
        )
        self.model.predict(np.zeros((1, 224, 224, 3)))

    '''
    Use vgg16 model to extract features
    Output normalized feature vector
    '''
    def extract_feat(self, img_path):
        if isinstance(img_path, str):
            img = image.load_img(img_path, target_size=(self.input_shape[0], self.input_shape[1]))
        else:
            img = img_path.resize((self.input_shape[0], self.input_shape[1]))

        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)  # mean-centering, scaling
        feat = self.model.predict(img)
        norm_feat = feat[0] / LA.norm(feat[0])  # L2 norm = 1
        return norm_feat


def rank_similar_images(queryImg, links):
    """
    Rank all images by similarity to query image
    
    Args:
        queryImg: PIL Image object
        links: List of [product_url, image_url, product_name, price]
    
    Returns:
        List of dicts with product_url, image_url, product_name, price, similarity_score
        Sorted from most similar to least similar
    """
    print("\n" + "=" * 60)
    print("VGG16 RANKING: Starting feature extraction...")
    print("=" * 60)
    
    model = VGGNet()
    features = []
    
    print(f"  → Processing {len(links)} product images...")
    
    for i, link in enumerate(links):
        try:
            product_url = link[0]
            image_url = link[1]
            product_name = link[2] if len(link) > 2 else "Unknown Product"
            price = link[3] if len(link) > 3 else "N/A"
            
            # Fetch image from URL
            print(f"  → [{i+1}/{len(links)}] Fetching: {product_name[:40]}...")
            response = requests.get(image_url, timeout=10)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            
            # Extract features
            vector = model.extract_feat(img)
            features.append(vector)
            
        except Exception as e:
            print(f"  ✗ Error processing image {i+1}: {e}")
            # Add zero vector for failed images so indices stay aligned
            features.append(np.zeros(512))  # VGG16 feature size
    
    print("✓ Feature extraction complete")
    
    # Extract features from query image
    print("  → Extracting features from query image...")
    query_feat = model.extract_feat(queryImg)
    print("✓ Query features extracted")
    
    # Calculate similarity scores
    print("  → Calculating similarity scores...")
    scores = []
    for i in range(len(features)):
        score = 1 - spatial.distance.cosine(query_feat, features[i])
        scores.append(score)
    
    scores = np.array(scores)
    print("✓ Similarity scores calculated")
    
    # Rank by similarity (highest to lowest)
    rank_ID = np.argsort(scores)[::-1]
    rank_score = scores[rank_ID]
    
    # Build results with ALL images, ranked
    results = []
    print("\n📊 Ranking Results:")
    print("-" * 60)
    
    for i, (image_id, score) in enumerate(zip(rank_ID, rank_score)):
        product_url = links[image_id][0]
        image_url = links[image_id][1]
        product_name = links[image_id][2] if len(links[image_id]) > 2 else "Unknown Product"
        price = links[image_id][3] if len(links[image_id]) > 3 else "N/A"
        
        result = {
            "rank": i + 1,
            "product_url": product_url,
            "image_url": image_url,
            "product_name": product_name,
            "price": price,
            "similarity_score": float(score)  # Convert to float for JSON serialization
        }
        
        results.append(result)
        
        # Print top 5 for debugging
        if i < 5:
            print(f"  {i+1}. {product_name[:40]}")
            print(f"     Score: {score:.4f} | Price: {price}")
            print(f"     URL: {product_url[:60]}...")
    
    print("-" * 60)
    print(f"✓ Total results: {len(results)}")
    print("=" * 60 + "\n")
    
    return results