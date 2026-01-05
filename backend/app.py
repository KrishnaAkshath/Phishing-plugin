from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import numpy as np
from feature_extraction import extract_features

# =========================
# APP CONFIG
# =========================
app = FastAPI(title="PhishGuard AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Chrome extension
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MODEL LOADING (SAFE)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

_model = None

def get_model():
    global _model
    if _model is None:
        print(f"🔄 Loading ML model from: {MODEL_PATH}")

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"❌ model.pkl not found at {MODEL_PATH}"
            )

        _model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully")

    return _model


# =========================
# REQUEST SCHEMA
# =========================
class URLRequest(BaseModel):
    url: str


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "status": "running",
        "service": "PhishGuard AI",
        "message": "API is live"
    }


# =========================
# PREDICTION ENDPOINT
# =========================
@app.post("/predict")
def predict_url(data: URLRequest):
    try:
        model = get_model()

        features = extract_features(data.url)
        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]

        if hasattr(model, "predict_proba"):
            confidence = max(model.predict_proba(features)[0])
        else:
            confidence = 0.75  # fallback

        label = "Phishing" if prediction == 1 else "Safe"

        return {
            "label": label,
            "confidence": round(float(confidence), 2)
        }

    except Exception as e:
        print("❌ Prediction error:", e)
        return {
            "error": str(e)
        }
