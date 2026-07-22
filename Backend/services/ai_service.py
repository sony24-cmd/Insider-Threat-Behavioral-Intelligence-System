import pandas as pd

from ai_model.model_loader import load_model

model = load_model()


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
    Predict insider threat risk using
    the trained Random Forest model.
    """

    data = pd.DataFrame([
        {
            "login_count": login_count,
            "logout_count": logout_count,
            "usb_connect": usb_connect,
            "usb_disconnect": usb_disconnect,
            "http_visits": http_visits,
            "suspicious_http_visits": suspicious_http_visits,
            "after_hours_events": after_hours_events,
            "unique_devices": unique_devices,
            "total_events": total_events,
        }
    ])

    prediction = model.predict(data)[0]

    probability = model.predict_proba(data)[0]

    confidence = round(max(probability) * 100, 2)

    risk_level = "High" if prediction == 1 else "Low"

    return {
        "prediction": int(prediction),
        "risk_level": risk_level,
        "confidence": confidence,
    }