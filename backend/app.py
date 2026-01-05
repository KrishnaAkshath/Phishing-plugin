from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os
from feature_extraction import extract_features

app = FastAPI(title="PhishGuard AI API")

# ✅ CORS for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Model Loader --------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
_model = None

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

# -------- Request Schema --------
class URLRequest(BaseModel):
    url: str

# -------- Health Check --------
@app.get("/")
def root():
    return {"status": "running"}

# -------- Prediction --------
@app.post("/predict")
def predict(data: URLRequest):
    model = get_model()
    features = extract_features(data.url)
    X = np.array(features).reshape(1, -1)

    pred = int(model.predict(X)[0])
    prob = float(max(model.predict_proba(X)[0]))

    return {
        "label": "Phishing" if pred == 1 else "Safe",
        "confidence": round(prob, 3)
    }
