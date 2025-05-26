
import clip
import torch
from PIL import Image


file_path = "/Users/shabichasureshkumar/Downloads/vans.jpg" #change image path for app
img = Image.open(file_path)

#upload image -> pass through category checks (colour, brand, object) through identification
#load CLIP


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

#load & preprocess
image = preprocess(Image.open(file_path)).unsqueeze(0).to(device)

#specialized search

colors = ["black", "white", "brown", "gray", "red", "green", "blue", "pink", "purple", "yellow", "beige", "orange"]
brands = ["Nike", "Adidas", "Zara", "Gucci", "H&M", "Levi's", "converse", "vans", "no brand"]
objects = ["hoodie", "jacket", "shirt", "jeans", "sneakers", "bag", "hat", "coat", "dress"]
def rank_clip_texts(texts, image, model):
    with torch.no_grad():
        text_tokens = clip.tokenize(texts).to(device)
        text_features = model.encode_text(text_tokens)
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (image_features @ text_features.T).squeeze()
    return texts[similarity.argmax()]
best_colour = rank_clip_texts(colors, image, model)
best_brand = rank_clip_texts(brands, image, model)
best_object = rank_clip_texts(objects, image, model)

descriptor = f"{best_colour} {best_brand} {best_object}"
print(descriptor)
