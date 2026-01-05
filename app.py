from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import sys, os
import requests

# Allow importing from ml folder
sys.path.append(os.path.abspath("../ml"))
from feature_extraction import extract_features

app = FastAPI()

MODEL_URL = "https://drive.google.com/uc?id=1YaaGFO7Vq9IxVCrRCbwt25YtAV--JZNH"
MODEL_PATH = "model.pkl"

# Download model if not present
if not os.path.exists(MODEL_PATH):
    print("⬇️ Downloading ML model...")
    r = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(r.content)
    print("✅ Model downloaded")

# Load model
model = joblib.load(MODEL_PATH)

class URLRequest(BaseModel):
    url: str

@app.post("/predict")
def predict(data: URLRequest):
    features = extract_features(data.url)
    X = pd.DataFrame([features])

    prob = model.predict_proba(X)[0][1]
    label = "Phishing" if prob >= 0.5 else "Safe"

    return {
        "label": label,
        "confidence": round(float(prob), 2)
    }

