import clip
import torch
from PIL import Image
from io import BytesIO

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

colors = ["black", "white", "brown", "gray", "red", "green", "blue", "pink", "purple", "yellow", "beige", "orange"]
brands = ["Nike", "Adidas", "Zara", "Gucci", "H&M", "Levi's", "converse", "vans", "no brand"]
objects = ["hoodie", "jacket", "shirt", "jeans", "sneakers", "bag", "hat", "coat", "dress"]

def rank_clip_texts(texts, image):
    with torch.no_grad():
        text_tokens = clip.tokenize(texts).to(device)
        text_features = model.encode_text(text_tokens)
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (image_features @ text_features.T).squeeze()
    return texts[similarity.argmax()]

def classify_image(img_bytes):
    image = preprocess(Image.open(img_bytes).convert("RGB")).unsqueeze(0).to(device)
    best_colour = rank_clip_texts(colors, image)
    best_brand = rank_clip_texts(brands, image)
    best_object = rank_clip_texts(objects, image)
    return best_colour, best_brand, best_object
