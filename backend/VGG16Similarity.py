#compare cosine similarity + rank
# VGG16 method to exctract image features
import numpy as np
from numpy import linalg as LA
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from flask import Flask, request, jsonify
from flask_cors import CORS



class VGGNet:
    def __init__(self):
        # weights: 'imagenet'
        # pooling: 'max' or 'avg'
        # input_shape: (width, height, 3), width and height should >= 48
        self.input_shape = (224, 224, 3)
        #weights pre-trained on the ImageNet dataset
        self.weight = 'imagenet'
        self.pooling = 'max'
        self.model = VGG16(weights = self.weight, input_shape = (self.input_shape[0], self.input_shape[1], self.input_shape[2]), pooling = self.pooling, include_top = False)
        self.model.predict(np.zeros((1, 224, 224 , 3)))


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
        img = preprocess_input(img) # mean-centering, scaling
        feat = self.model.predict(img)
        norm_feat = feat[0]/LA.norm(feat[0]) #L2 norm = 1
        return norm_feat

#read images & return features for image database
import h5py
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import os
def rank_similar_images(queryImg, links):
    model = VGGNet()
    features = []
    names = []
    
    for i in range(len(links)):
        url = links[i][1]
        name = links[i][0]
        
        # Fetch img from URL
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGB")  # ✅ FIX: Use response.content
        
        print("Extracting features from image - ", name)
        vector = model.extract_feat(img)

        features.append(vector)
        names.append(name)

    # directory for storing extracted features
    output = "CNNFeatures.h5"
    print("writing feature extraction results to h5 file")

    h5f = h5py.File(output, 'w')
    h5f.create_dataset('dataset_1', data=features)
    h5f.create_dataset('dataset_2', data=np.bytes_(names))
    h5f.close()

    # Reading from h5 file
    h5f = h5py.File("CNNFeatures.h5",'r')
    feats = h5f['dataset_1'][:]
    imgNames = h5f['dataset_2'][:]
    print(feats)
    print(imgNames)
    print(len(imgNames))
    h5f.close()

    # Compare image feature dataset with user inputted image
    query_feat = model.extract_feat(queryImg)  # ✅ This is correct now
    print("Extracting features from query image")

    scores = []
    from scipy import spatial
    for i in range(feats.shape[0]):
        score = 1-spatial.distance.cosine(query_feat, feats[i])
        scores.append(score)
    
    scores = np.array(scores)
    rank_ID = np.argsort(scores)[::-1]
    rank_score = scores[rank_ID]

    # Get top 3 matches
    top_n = 3
    top_matches = rank_ID[:top_n]
    top_scores = rank_score[:top_n]

    # Print matches
    results = []
    print(f"Top {top_n} matches with similarity scores:")
    for i, (image_id, score) in enumerate(zip(top_matches, top_scores)):
        if isinstance(imgNames[image_id], bytes):
            image_name = imgNames[image_id].decode('utf-8') 
        else:
            image_name = imgNames[image_id]
        print(f"{i+1}. Image: {image_name}, Score: {score:.4f}")
        results.append([image_name, links[image_id][1]])

    print("Results: ", results)
    return results