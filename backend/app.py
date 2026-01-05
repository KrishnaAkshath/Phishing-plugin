from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
import requests
import tempfile
import numpy as np

from feature_extraction import extract_features

app = FastAPI()

MODEL_URL = os.getenv(
    "MODEL_URL",
    "https://drive.google.com/uc?id=1i6z9Wc1pCN_VH-ZofqOqdV5VWKKUU03B"
)

MODEL_PATH = "model.pkl"
model = None


class URLRequest(BaseModel):
    url: str


def download_model():
    global model

    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("[+] Model loaded from disk")
        return

    print("[*] Downloading model from Google Drive...")
    r = requests.get(MODEL_URL, timeout=30)
    r.raise_for_status()

    with open(MODEL_PATH, "wb") as f:
        f.write(r.content)

    model = joblib.load(MODEL_PATH)
    print("[+] Model downloaded & loaded")


@app.on_event("startup")
def startup():
    download_model()


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: URLRequest):
    try:
        features = extract_features(req.url)
        X = np.array([features])

        prediction = model.predict(X)[0]

        # 🧠 Normalize output
        if prediction in [1, "bad", "phishing", True]:
            label = "Phishing"
            confidence = 0.85
        else:
            label = "Safe"
            confidence = 0.90

        return {
            "label": label,
            "confidence": confidence
        }

    except Exception as e:
        return {"error": str(e)}
