from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import numpy as np

from feature_extraction import extract_features
from train_model import train_and_save_model

app = FastAPI(title="PhishGuard AI API")

# ✅ REQUIRED FOR CHROME EXTENSION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "model.pkl"
_model = None

def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            print("⚠️ model.pkl not found — training now")
            train_and_save_model()
        _model = joblib.load(MODEL_PATH)
        print("✅ Model loaded")
    return _model

class URLRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/predict")
def predict(data: URLRequest):
    model = get_model()

    features = np.array(
        extract_features(data.url)
    ).reshape(1, -1)

    pred = model.predict(features)[0]
    confidence = float(max(model.predict_proba(features)[0]))

    return {
        "label": "Phishing" if pred == 1 else "Safe",
        "confidence": round(confidence, 2)
    }
