from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
from feature_extraction import extract_features
import numpy as np

app = FastAPI(title="PhishGuard AI API")

# ✅ CORS FIX (REQUIRED FOR CHROME EXTENSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

        prediction = model.predict(feature
