from flask import Flask, render_template, request, jsonify
import os
import base64
import json
import cv2
import numpy as np

app = Flask(__name__)

DATA_FILE = os.path.join("data", "users.json")
IMAGES_DIR = os.path.join("data", "faces")
os.makedirs(IMAGES_DIR, exist_ok=True)

# Use OpenCV's built-in Haar cascade for face detection
FACE_CASCADE_PATH = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)


def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)


def compute_face_signature(img):
    """Compute a simple color histogram-based signature for a face image.

    This is not as strong as deep learning, but is enough to roughly
    detect if the same person tries to register again on this demo.
    """
    # Resize to reduce noise and computation
    resized = cv2.resize(img, (128, 128))
    # Convert to HSV color space and compute histogram
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [32, 32], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    # Flatten to 1D list so it can be stored in JSON
    return hist.flatten().tolist()


@app.route("/")
def index():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    image_data = data.get("image")

    if not username or not image_data:
        return jsonify({"success": False, "message": "Missing username or image"}), 400

    # Load existing users once
    users = load_users()

    # Enforce unique username
    for u in users:
        if u.get("username") == username:
            return jsonify({"success": False, "message": "Username already registered"}), 400

    try:
        header, encoded = image_data.split(",", 1)
    except ValueError:
        return jsonify({"success": False, "message": "Bad image format"}), 400

    img_bytes = base64.b64decode(encoded)
    img_array = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"success": False, "message": "Invalid image"}), 400

    # Convert to grayscale for Haar cascade
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        return jsonify({"success": False, "message": "No face detected"}), 400
    if len(faces) > 1:
        return jsonify({"success": False, "message": "Multiple faces detected"}), 400

    filename = f"{username}.png"
    filepath = os.path.join(IMAGES_DIR, filename)
    cv2.imwrite(filepath, img)

    # Compute a simple face signature for duplicate-face detection
    new_sig = compute_face_signature(img)

    # Check if this face is already in the system (approximate check)
    for u in users:
        stored_sig = u.get("signature")
        if stored_sig is None:
            continue
        sig_array = np.array(stored_sig, dtype=np.float32)
        new_array = np.array(new_sig, dtype=np.float32)
        # Compare histograms using correlation; 1.0 = identical
        sim = cv2.compareHist(sig_array.astype("float32"), new_array.astype("float32"), cv2.HISTCMP_CORREL)
        if sim > 0.95:
            # Treat as same face already registered
            return jsonify({
                "success": False,
                "message": "This face is already registered (ID: {}, Name: {}).".format(u.get("id"), u.get("username"))
            }), 400

    # Assign a unique integer id
    if users:
        max_id = max((u.get("id", 0) for u in users))
    else:
        max_id = 0
    new_id = max_id + 1

    users.append({"id": new_id, "username": username, "image": filename, "signature": new_sig})
    save_users(users)

    return jsonify({"success": True, "message": "User registered successfully", "id": new_id, "username": username})


if __name__ == "__main__":
    app.run(debug=True)
