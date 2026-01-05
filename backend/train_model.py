import os
import requests
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from feature_extraction import extract_features

DATASET_URL = "https://drive.google.com/uc?export=download&id=1YaaGFO7Vq9IxVCrRCbwt25YtAV--JZNH"
DATASET_PATH = "dataset.csv"
MODEL_PATH = "model.pkl"

def download_dataset():
    if not os.path.exists(DATASET_PATH):
        print("⬇️ Downloading dataset from Google Drive...")
        response = requests.get(DATASET_URL)
        with open(DATASET_PATH, "wb") as f:
            f.write(response.content)
        print("✅ Dataset downloaded")

def train_model():
    download_dataset()

    print("📊 Loading dataset...")
    df = pd.read_csv(DATASET_PATH)

    print("🧹 Cleaning labels...")
    df["label"] = df["label"].replace({
        "bad": 1,
        "good": 0
    })

    print("⚙️ Extracting features...")
    X = df["url"].apply(extract_features).tolist()
    y = df["label"]

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("🧠 Training RandomForest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        n_jobs=-1,
        random_state=42
    )
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)
    print("✅ model.pkl saved successfully")

def ensure_model_exists():
    if not os.path.exists(MODEL_PATH):
        print("⚠️ model.pkl not found — training model now")
        train_model()
