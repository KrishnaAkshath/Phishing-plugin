import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from feature_extraction import extract_features

print("[*] Loading dataset...")
df = pd.read_csv("dataset.csv")

# Explicit column names (based on your dataset)
url_col = "URL"
label_col = "Label"

print("[*] Unique labels before cleaning:", df[label_col].unique())

# Normalize labels
df[label_col] = df[label_col].astype(str).str.lower().str.strip()

df[label_col] = df[label_col].replace({
    "bad": 1,
    "phishing": 1,
    "malicious": 1,
    "good": 0,
    "legitimate": 0,
    "benign": 0
})

# Convert labels to numeric
df[label_col] = pd.to_numeric(df[label_col], errors="coerce")

# Drop rows with invalid labels or URLs
df = df.dropna(subset=[url_col, label_col])

print("[*] Samples after cleaning:", len(df))

if len(df) < 50:
    raise ValueError("❌ Too few samples after cleaning. Check dataset.")

print("[*] Extracting features...")
X = df[url_col].apply(extract_features)
X = pd.DataFrame(list(X))
y = df[label_col]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("[*] Training model...")
model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)
model.fit(X_train, y_train)

preds = model.predict(X_test)
accuracy = accuracy_score(y_test, preds)

print(f"[+] Model Accuracy: {accuracy:.2f}")

joblib.dump(model, "model.pkl")
print("[+] model.pkl saved successfully")

