from flask import Flask, request, jsonify
from flask_cors import CORS
from CLIPFeatureIdentify import classify_image
from depopScraper import get_depop_links
from VGG16Similarity import rank_similar_images
from PIL import Image
from io import BytesIO
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        print("=" * 60)
        print("RECEIVED REQUEST")
        print("=" * 60)
        
        # Check if image exists
        if 'image' not in request.files:
            print("✗ ERROR: No image in request")
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['image']
        print(f"✓ Image received: {file.filename}")
        
        # Read and open image
        print("  → Reading image bytes...")
        file_bytes = file.read()
        print(f"✓ Image size: {len(file_bytes)} bytes")
        
        print("  → Opening image with PIL...")
        img_bytes = Image.open(BytesIO(file_bytes)).convert("RGB")
        print(f"✓ Image opened: {img_bytes.size}")

        # CLIP classification
        print("\n" + "=" * 60)
        print("STAGE 1: CLIP Classification")
        print("=" * 60)
        best_colour, best_brand, best_object = classify_image(img_bytes)
        print(f"✓ Classification complete:")
        print(f"  Color: {best_colour}")
        print(f"  Brand: {best_brand}")
        print(f"  Object: {best_object}")

        # Scrape Depop
        print("\n" + "=" * 60)
        print("STAGE 2: Scraping Depop")
        print("=" * 60)
        depop_links = get_depop_links(best_colour, best_brand, best_object)
        print(f"✓ Scraping complete: {len(depop_links)} links found")

        if not depop_links:
            print("✗ ERROR: No listings found")
            return jsonify({"error": "No listings found"}), 404

        # Rank with VGG16
        print("\n" + "=" * 60)
        print("STAGE 3: VGG16 Ranking")
        print("=" * 60)
        results = rank_similar_images(img_bytes, depop_links)
        print(f"✓ Ranking complete: {len(results)} results")

        print("\n" + "=" * 60)
        print("SUCCESS - Returning results")
        print("=" * 60)
        
        # Return with metadata
        return jsonify({
            "total_results": len(results),
            "results": results
        })

    except Exception as e:
        print("\n" + "=" * 60)
        print("✗✗✗ FATAL ERROR ✗✗✗")
        print("=" * 60)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nFull traceback:")
        print(traceback.format_exc())
        print("=" * 60)
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)