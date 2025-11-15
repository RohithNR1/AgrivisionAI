from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import base64
import io
from PIL import Image
import os
import requests
from datetime import datetime

# ================= Flask Setup =================
app = Flask(__name__, static_folder="vision-agri-care-main/dist", static_url_path="")
CORS(app)

# ================= Gemini API Setup =================
API_KEY = os.environ.get("GEMINI_API_KEY") or "AIzaSyBzZiW0njEOfWPxABbyiDtQioMRUUor8tw"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def gemini_response(message):
    params = {"key": API_KEY}
    data = {"contents": [{"parts": [{"text": message}]}]}
    try:
        resp = requests.post(GEMINI_URL, params=params, json=data)
        if resp.status_code == 200:
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Gemini error: {resp.text}"
    except Exception as e:
        return f"Gemini API error: {e}"

@app.route('/api/chat', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message', '')
    response_text = gemini_response(user_message)
    return jsonify({"response": response_text, "timestamp": str(datetime.now())})

# ================= Model Setup =================
model_path = os.path.join(os.path.dirname(__file__), "plant_disease_model_fixed.keras")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at path: {model_path}")

model = load_model(model_path, compile=False)

class_names = [
"Apple___Apple_scab",
"Apple___Black_rot",
"Apple___Cedar_apple_rust",
"Apple___healthy",
"Blueberry___healthy",
"Cherry_(including_sour)___Powdery_mildew",
"Cherry_(including_sour)___healthy",
"Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
"Corn_(maize)___Common_rust_",
"Corn_(maize)___Northern_Leaf_Blight",
"Corn_(maize)___healthy",
"Grape___Black_rot",
"Grape___Esca_(Black_Measles)",
"Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
"Grape___healthy",
"Orange___Haunglongbing_(Citrus_greening)",
"Peach___Bacterial_spot",
"Peach___healthy",
"Pepper,_bell___Bacterial_spot",
"Pepper,_bell___healthy",
"Potato___Early_blight",
"Potato___Late_blight",
"Potato___healthy",
"Raspberry___healthy",
"Soybean___healthy",
"Squash___Powdery_mildew",
"Strawberry___Leaf_scorch",
"Strawberry___healthy",
"Tomato___Bacterial_spot",
"Tomato___Early_blight",
"Tomato___Late_blight",
"Tomato___Leaf_Mold",
"Tomato___Septoria_leaf_spot",
"Tomato___Spider_mites Two-spotted_spider_mite",
"Tomato___Target_Spot",
"Tomato___Tomato_Yellow_Leaf_Curl_Virus",
"Tomato___Tomato_mosaic_virus",
"Tomato___healthy"
]



# ================= Treatment Data =================
treatment_data = {
    "Apple___Apple_scab": {
        "treatments": [
            "Spray fungicides like mancozeb, captan, or myclobutanil during early leaf stages.",
            "Remove fallen leaves to reduce fungal spores.",
            "Use resistant apple varieties."
        ],
        "remedies": [
            "Apply neem oil every 10–14 days.",
            "Use baking soda spray (1 tsp per litre of water)."
        ],
        "prevention": [
            "Avoid overhead irrigation.",
            "Ensure good air circulation by pruning trees."
        ],
        "severity": "medium"
    },
    "Potato___Late_blight": {
        "treatments": [
            "Spray copper-based fungicides or chlorothalonil every 7–10 days.",
            "Remove and destroy infected leaves.",
            "Improve air flow around plants."
        ],
        "remedies": [
            "Neem oil or baking soda spray for mild cases.",
            "Use resistant potato varieties."
        ],
        "prevention": [
            "Avoid overhead watering.",
            "Rotate crops annually to prevent soil-borne infection."
        ],
        "severity": "high"
    },
    "Tomato___Early_blight": {
        "treatments": [
            "Apply fungicides like chlorothalonil or copper oxychloride weekly.",
            "Prune infected leaves and dispose away from field."
        ],
        "remedies": [
            "Use neem oil or garlic-based sprays.",
            "Ensure good spacing for ventilation."
        ],
        "prevention": [
            "Rotate crops and avoid wetting leaves while watering.",
            "Mulch around plants to reduce soil splash."
        ],
        "severity": "medium"
    },
    "Tomato___Leaf_Mold": {
        "treatments": [
            "Use fungicides containing copper or potassium bicarbonate.",
            "Improve air circulation by pruning lower leaves."
        ],
        "remedies": [
            "Neem oil and baking soda spray (weekly)."
        ],
        "prevention": [
            "Avoid high humidity in greenhouses.",
            "Use resistant tomato varieties."
        ],
        "severity": "medium"
    }
}

# ================= Helper Functions =================
def preprocess_image(image_data):
    if ',' in image_data:
        image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize((224, 224))
    img_array = img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)

def find_treatment(predicted_class):
    if predicted_class in treatment_data:
        return treatment_data[predicted_class]
    for key in treatment_data.keys():
        if key.split('___')[0].lower() in predicted_class.lower() or key.split('___')[1].split('(')[0].lower() in predicted_class.lower():
            return treatment_data[key]
    return {
        "treatments": ["Consult with a local agricultural extension office"],
        "remedies": ["General plant care and monitoring"],
        "prevention": ["Follow good agricultural practices"],
        "severity": "medium"
    }

# ================= API Routes =================
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400

        processed_image = preprocess_image(data['image'])
        predictions = model.predict(processed_image)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]) * 100)
        predicted_class = class_names[predicted_class_idx]

        is_healthy = 'healthy' in predicted_class.lower()
        treatment = None if is_healthy else find_treatment(predicted_class)

        result = {
            'disease': predicted_class.replace('_', ' ').replace('  ', ' '),
            'confidence': round(confidence, 2),
            'isHealthy': is_healthy,
            'treatment': treatment
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Plant Disease Detection API is running'})

# ================= Serve Frontend =================
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# ================= Main =================
if __name__ == '__main__':
    print("🌱 Starting Plant Disease Detection API...")
    print(f"📂 Model loaded from: {model_path}")
    print(f"🌾 Number of classes: {len(class_names)}")
    app.run(host='0.0.0.0', port=5000)
