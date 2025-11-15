🌱 AgriVisionAI – Plant Disease Detection & Smart Farming Assistant

AgriVisionAI is an AI-powered plant disease detection system that helps farmers and agricultural researchers identify plant diseases using deep learning and provides actionable treatment suggestions.
The system includes:

✔️ A trained MobileNetV2 deep learning model
✔️ A Flask backend API to process images
✔️ A React + Vite frontend interface
✔️ Real-time prediction, preview, and recommended treatments
✔️ Chatbot support for basic farming queries

🚀 Features
🔍 Plant Disease Detection

Upload an image of a crop leaf

Deep learning model predicts the disease

Shows confidence percentage

🧠 AI-Powered Model

MobileNetV2-based CNN model

Trained on PlantVillage dataset (38 classes)

GPU-optimized & fine-tuned

Exported as:

plant_disease_model_fixed.keras

class_names.json

💬 Chat Assistant

Simple farming assistant built into the UI

Helps users with tips and general guidance

🌐 Modern Frontend

Built with React + Vite + Shadcn UI

Fast, clean, mobile-friendly interface

🔗 Backend API

Flask server at http://localhost:5000/predict

Accepts images via POST request

Returns predicted class + confidence

📁 Project Structure
AgriVisionAI-main/
│── backend.py                # Flask API server
│── backend_mock.py           # Mock backend (testing)
│── plant_disease_model_fixed.keras
│── class_names.json
│── requirements.txt
│── venv/ or tfenv/           # Virtual environment
│
└── vision-agri-care-main/    # React frontend (Vite)
    ├── src/
    ├── package.json
    ├── vite.config.ts
    └── ...

⚙️ Installation & Setup
1️⃣ Backend Setup (Flask + TensorFlow)
cd AgriVisionAI-main
pip install -r requirements.txt
python backend.py


Server runs at:
👉 http://127.0.0.1:5000

2️⃣ Frontend Setup (React + Vite)
cd vision-agri-care-main
npm install
npm run dev


App runs at:
👉 http://localhost:8080

🧪 Usage

Start backend (python backend.py)

Start frontend (npm run dev)

Open app in browser

Upload a plant leaf picture

Get disease name + confidence

View treatment suggestions

📊 Results

Model trained for 5 warmup epochs + 12 finetune epochs

Dataset: PlantVillage (38 classes)

Achieved high accuracy after fine-tuning

Works well for most tomato, potato, grape, and citrus diseases

🛠️ Tech Stack
Frontend

React + TypeScript

Vite

Shadcn UI

TailwindCSS

Backend

Python

Flask

TensorFlow / Keras

Pillow

Model

MobileNetV2

Fine-tuned on 38 disease classes

👤 Author

Rohith N R
4th Semester – Information Science & Engineering
Built as part of an academic Machine Learning + Full-Stack project

⭐ Contribute

Pull requests are welcome!
If you find a bug or want a new feature, open an issue.
