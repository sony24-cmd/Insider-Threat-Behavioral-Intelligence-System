import pandas as pd

from ai_model.model_loader import load_model

# ==========================================
# Load Trained Model
# ==========================================

model = load_model()


# ==========================================
# Predict Employee Risk
# ==========================================

def predict_risk(
    login_count: int,
    logout_count: int,
    usb_connect: int,
    usb_disconnect: int,
    http_visits: int,
    suspicious_http_visits: int,
    after_hours_events: int,
    unique_devices: int,
    total_events: int,
):
    """
    Predict insider threat risk using the trained AI model.
    """

    sample = pd.DataFrame(
        [[
            login_count,
            logout_count,
            usb_connect,
            usb_disconnect,
            http_visits,
            suspicious_http_visits,
            after_hours_events,
            unique_devices,
            total_events,
        ]],
        columns=[
            "login_count",
            "logout_count",
            "usb_connect",
            "usb_disconnect",
            "http_visits",
            "suspicious_http_visits",
            "after_hours_events",
            "unique_devices",
            "total_events",
        ],
    )

    prediction = int(model.predict(sample)[0])

    confidence = float(
        model.predict_proba(sample)[0][prediction]
    )

    return {
        "prediction": prediction,
        "confidence": round(confidence, 4),
        "risk_level": (
            "High Risk"
            if prediction == 1
            else "Low Risk"
        ),
    }