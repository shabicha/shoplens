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
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['image']
        file_bytes = file.read()

        print("✅ Image received, bytes:", len(file_bytes))

        img = Image.open(BytesIO(file_bytes)).convert("RGB")
        print("✅ Image loaded")

        print("➡️ Running CLIP...")
        best_colour, best_brand, best_object = classify_image(img)
        print("✅ CLIP done:", best_colour, best_brand, best_object)

        print("➡️ Scraping depop...")
        depop_links = get_depop_links(best_colour, best_brand, best_object)
        print("✅ Depop scraping done")

        if not depop_links:
            return jsonify({"error": "No listings found"}), 404

        print("➡️ Ranking images...")
        results = rank_similar_images(img, depop_links)
        print("✅ Ranking done")

        return jsonify({"results": results})

    except Exception as e:
        print("🔥 BACKEND ERROR 🔥")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
