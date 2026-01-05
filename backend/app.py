from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import joblib
import numpy as np
from feature_extraction import extract_features
from train_model import ensure_model_exists

app = FastAPI(title="PhishGuard AI API")

# ---------- CORS (Chrome Extension Fix) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "model.pkl"

# ---------- Request Schema ----------
class URLRequest(BaseModel):
    url: str

# ---------- Health Check ----------
@app.get("/")
def root():
    return {
        "status": "running",
        "service": "PhishGuard AI",
        "message": "API is live"
    }

# ---------- Prediction Endpoint ----------
@app.post("/predict")
def predict_url(data: URLRequest):
    try:
        # 🔥 Auto-train model if missing
        ensure_model_exists()

        model = joblib.load(MODEL_PATH)

        features = extract_features(data.url)
        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]
        confidence = max(model.predict_proba(features)[0])

        return {
            "label": "Phishing" if prediction == 1 else "Safe",
            "confidence": round(float(confidence), 2)
        }

    except Exception as e:
        return {"error": str(e)}
