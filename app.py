03.21 6:11 AM
App.py
from flask import Flask, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load pre-trained models for gender and age detection
gender_model = load_model("gender_model.h5")
age_model = load_model("age_model.h5")

# Enhanced Dress Data
dresses = [
    {"name": "Men's Suit", "image": "https://via.placeholder.com/150x200", "category": "male", "type": "formal", "color": "black", "size": ["S", "M", "L"], "price": 120.00, "bodyShape": ["slim", "athletic"], "ageGroup": ["young", "adult"]},
    {"name": "Women's Evening Gown", "image": "https://via.placeholder.com/150x200", "category": "female", "type": "formal", "color": "red", "size": ["S", "M", "L"], "price": 150.00, "bodyShape": ["curvy", "hourglass"], "ageGroup": ["young", "adult"]},
    {"name": "Boys T-Shirt", "image": "https://via.placeholder.com/150x200", "category": "child_male", "type": "casual", "color": "blue", "size": ["4", "6", "8"], "price": 20.00, "bodyShape": ["slim"], "ageGroup": ["child"]},
    {"name": "Girls Dress", "image": "https://via.placeholder.com/150x200", "category": "child_female", "type": "casual", "color": "pink", "size": ["4", "6", "8"], "price": 25.00, "bodyShape": ["slim"], "ageGroup": ["child"]},
    {"name": "Elderly Men's Jacket", "image": "https://via.placeholder.com/150x200", "category": "male", "type": "formal", "color": "navy", "size": ["L", "XL"], "price": 80.00, "bodyShape": ["athletic", "broad"], "ageGroup": ["old"]},
    {"name": "Elderly Women's Dress", "image": "https://via.placeholder.com/150x200", "category": "female", "type": "formal", "color": "purple", "size": ["L", "XL"], "price": 90.00, "bodyShape": ["curvy", "hourglass"], "ageGroup": ["old"]}
]

# Function to detect gender and age using TensorFlow models
def detect_gender_age(image):
    # Preprocess the image
    resized_image = cv2.resize(image, (128, 128))
    normalized_image = resized_image / 255.0
    input_image = np.expand_dims(normalized_image, axis=0)

    # Predict gender
    gender_pred = gender_model.predict(input_image)
    gender = "male" if gender_pred[0][0] > 0.5 else "female"

    # Predict age
    age_pred = age_model.predict(input_image)
    age_group = "child" if age_pred[0][0] < 18 else "adult" if age_pred[0][0] < 60 else "old"

    return gender, age_group

# Mock function to detect body shape
def detect_body_shape(image):
    # Placeholder logic (replace with a real model if needed)
    body_shape = "slim" if np.random.rand() > 0.5 else "curvy"
    return body_shape

# Function to recommend dresses
def recommend_dresses(gender, age_group, body_shape):
    category = gender
    if age_group == "child":
        category = f"child_{gender}"
    elif age_group == "old":
        category = f"elderly_{gender}"

    recommended_dresses = [dress for dress in dresses if dress["category"] == category and body_shape in dress["bodyShape"] and age_group in dress["ageGroup"]]
    return recommended_dresses

# Flask Routes
@app.route("/")
def home():
    return "Dress Recommender Backend"

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Detect attributes
    gender, age_group = detect_gender_age(image)
    body_shape = detect_body_shape(image)

    # Recommend dresses
    recommended_dresses = recommend_dresses(gender, age_group, body_shape)
    return jsonify({"gender": gender, "age_group": age_group, "body_shape": body_shape, "recommended_dresses": recommended_dresses})

if __name__ == "__main__":
    app.run(debug=True)
