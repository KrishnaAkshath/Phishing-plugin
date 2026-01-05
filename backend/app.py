from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from feature_extraction import extract_features
import os

app = FastAPI(title="PhishGuard AI API")

# ---------- CORS (required for Chrome extension) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # OK for demo / hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Load model lazily ----------
MODEL_PATH = "model.pkl"
_model = None

def get_model():
    global _model
    if _model is None:
        print("🔄 Loading ML model...")
        _model = joblib.load(MODEL_PATH)
        print("✅ Model loaded")
    return _model


# ---------- Request schema ----------
class URLRequest(BaseModel):
    url: str


# ---------- Health check ----------
@app.get("/")
def root():
    return {
        "status": "running",
        "service": "PhishGuard AI",
        "message": "API is live"
    }


# ---------- Prediction endpoint ----------
@app.post("/predict")
def predict_url(data: URLRequest):
    try:
        model = get_model()

        features = extract_features(data.url)
        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = float(max(probabilities))

        label = "Phishing" if prediction == 1 else "Safe"

        return {
            "label": label,
            "confidence": round(confidence, 2)
        }

    except Exception as e:
        return {
            "error": str(e)
        }
