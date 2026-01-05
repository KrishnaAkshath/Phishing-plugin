import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from feature_extraction import extract_features

def train_and_save_model():
    print("📊 Loading dataset...")
    df = pd.read_csv("dataset.csv")

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

    print("🧠 Training model...")
    model = RandomForestClassifier(
        n_estimators=100,
        n_jobs=-1,
        random_state=42
    )
    model.fit(X_train, y_train)

    joblib.dump(model, "model.pkl")
    print("✅ model.pkl trained and saved")
