from ai_model.utils import load_model

def load_trained_model():
    return load_model("insider_model.pkl")

def load_scaler():
    return load_model("scaler.pkl")

def load_encoder():
    return load_model("label_encoder.pkl")