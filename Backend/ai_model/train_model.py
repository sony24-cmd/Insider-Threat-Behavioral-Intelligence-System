import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split


# ==========================================
# Load Feature Dataset
# ==========================================

df = pd.read_csv("ai_model/employee_features.csv")

# ==========================================
# Create Labels (Temporary)
# ==========================================

df["risk"] = 0

df.loc[df["total_events"] >= 15, "risk"] = 1

# ==========================================
# Features
# ==========================================

FEATURE_COLUMNS = [
    "login_count",
    "logout_count",
    "usb_connect",
    "usb_disconnect",
    "http_visits",
    "suspicious_http_visits",
    "after_hours_events",
    "unique_devices",
    "total_events",
]

X = df[FEATURE_COLUMNS]
y = df["risk"]

# ==========================================
# Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# ==========================================
# Train Model
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
)

model.fit(X_train, y_train)

# ==========================================
# Evaluate Model
# ==========================================

predictions = model.predict(X_test)

print("\n========== MODEL EVALUATION ==========")

print(f"\nAccuracy : {accuracy_score(y_test, predictions):.2f}")

print("\nConfusion Matrix")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report")
print(classification_report(y_test, predictions))

print("\nFeature Importance")

for feature, importance in zip(
    FEATURE_COLUMNS,
    model.feature_importances_,
):
    print(f"{feature:<30} {importance:.4f}")

# ==========================================
# Save Model
# ==========================================

joblib.dump(
    model,
    "ai_model/risk_model.pkl",
)

print("\n======================================")
print("Model trained successfully!")
print("Saved -> ai_model/risk_model.pkl")
print("======================================")