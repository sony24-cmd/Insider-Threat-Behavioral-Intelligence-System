import joblib
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "risk_model.pkl",
)


def load_model():
    """
    Load the trained Random Forest model.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)