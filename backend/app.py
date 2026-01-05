from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
from feature_extraction import extract_features
import numpy as np

app = FastAPI(title="PhishGuard AI API")

# --------- Lazy-loaded model ---------
_model = None

def get_model():
    global _model
    if _model is None:
        print("🔄 Loading ML model...")
        _model = joblib.load("model.pkl")
        print("✅ Model loaded")
    return _model


# --------- Request schema ---------
class URLRequest(BaseModel):
    url: str


# --------- Health check ---------
@app.get("/")
def root():
    return {
        "status": "running",
        "service": "PhishGuard AI",
        "message": "API is live"
    }


# --------- Prediction endpoint ---------
@app.post("/predict")
def predict_url(data: URLRequest):
    try:
        model = get_model()

        features = extract_features(data.url)
        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]
        confidence = max(model.predict_proba(features)[0])

        label = "Phishing" if prediction == 1 else "Safe"

        return {
            "label": label,
            "confidence": round(float(confidence), 2)
        }

    except Exception as e:
        return {
            "error": str(e)
        }
