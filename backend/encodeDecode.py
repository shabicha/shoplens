
from PIL import Image
from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('clip-ViT-B-32')  #  image + text support


def encode_image(image_path):
    image = Image.open(image_path).convert("RGB")
    return model.encode(image, convert_to_tensor=True)

#shopify dummy data
shopify_products = [
    {"title": "Red Converse", "description": "Trendy red sneakers."},
    {"title": "White Ribbed Crop Top", "description": "A trendy white crop top with ribbed texture."},
    {"title": "Beige Trench Coat", "description": "A classic beige trench for spring."},
    {"title": "High-Waisted Blue Jeans", "description": "Stylish high-rise jeans in vintage wash."}
]

descriptions = [p["description"] for p in shopify_products]
text_embeddings = model.encode(descriptions, convert_to_tensor=True)
#returns product matches/compute similarity
#!!!"Fast Approximate Nearest Neighbor Search" to not have to iterate individually through every article in shopify data
def match_image_to_products(image_path, top_k=2):
    image_embedding = encode_image(image_path)
    similarities = util.cos_sim(image_embedding, text_embeddings)[0]  # user image vs. each product
    top_indices = torch.topk(similarities, k=top_k).indices
    return [shopify_products[i] for i in top_indices]

results = match_image_to_products("/Users/shabichasureshkumar/Downloads/shoe.jpg")

for product in results:
    print(f"{product['title']} — {product['description']}")