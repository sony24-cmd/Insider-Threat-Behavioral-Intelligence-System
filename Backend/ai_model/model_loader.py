import joblib

MODEL_PATH = "ai_model/risk_model.pkl"


def load_model():
    """
    Load the trained Random Forest model.
    """
    return joblib.load(MODEL_PATH)