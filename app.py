from deepface import DeepFace
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# OPTIONAL: Test a static pair once at startup
try:
    result = DeepFace.verify(
        r"known_faces/virat.png",
        r"known_faces/ronaldo.jpg"
    )
    print("Is the person in the images the same? ", result['verified'])
except Exception as e:
    print("Startup check failed:", e)

@app.route("/detect-face", methods=["POST"])
def verify():
    # ✅ accept file upload too
    if "image" in request.files:
        file = request.files["image"]
        # Save to temp file or pass directly
        temp_path = "temp_uploaded.jpg"
        file.save(temp_path)
        img = temp_path
    else:
        # fallback to JSON body
        data = request.json
        img = data.get("img")

    if not img:
        return jsonify({"error": "Image is required"}), 400

    # loop over known_faces
    for known_face in os.listdir("known_faces"):
        known_face_path = os.path.join("known_faces", known_face)
        result = DeepFace.verify(img1_path=img, img2_path=known_face_path)
        if result['verified']:
            return jsonify({
                "verified": True,
                "matched_face": known_face,
                "distance": result['distance'],
                "model": result['model']
            })
        
    # # if mismatch, log it,save it in unknown_faces
    # print(f"Face in {known_face} did not match with uploaded image.")
    # unknown_faces_dir = "unknown_faces"
    # if not os.path.exists(unknown_faces_dir):
    #     os.makedirs(unknown_faces_dir)
    # unknown_face_path = os.path.join(unknown_faces_dir, f"unknown_{known_face}")
    # file.save(unknown_face_path)
    

    return jsonify({"verified": False})

if __name__ == "__main__":
    print("🔁 Loading known faces from ./known_faces ...")
    if not os.path.exists("known_faces"):
        print("⚠️  known_faces folder does not exist!")
    else:
        print(f"Found {len(os.listdir('known_faces'))} known faces")

    print("🚀 Server running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
