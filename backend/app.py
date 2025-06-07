from flask import Flask, request, jsonify
from flask_cors import CORS
from CLIPFeatureIdentify import classify_image
from depopScraper import get_depop_links
from VGG16Similarity import rank_similar_images
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    img_bytes = BytesIO(file.read())
    

    try:
        # CLIP to classify image (reduce batch size)
        
        best_colour, best_brand, best_object = classify_image(img_bytes)

        # Scrape Depop products based on CLIP classification
        depop_links = get_depop_links(best_colour, best_brand, best_object)
        print("done scraping depop links")

        if not depop_links:
            return jsonify({"error": "No listings found"}), 404

        # Rank scraped images by VGG16 similarity
        print("ranking images from app.py")
        results = rank_similar_images(img_bytes, depop_links)
        print(f"Results: {results}")

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
