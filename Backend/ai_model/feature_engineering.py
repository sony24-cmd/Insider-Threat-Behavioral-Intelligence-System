import pandas as pd
from datetime import datetime

from preprocessing import load_employee_logs


# ==========================================
# Suspicious Websites
# ==========================================

SUSPICIOUS_KEYWORDS = [
    "wikileaks",
    "secret",
    "classified",
    "confidential",
    "spy",
    "top-secret",
]


# ==========================================
# Feature Extraction
# ==========================================

def extract_features():

    logs = load_employee_logs()

    employee_features = []

    for employee, events in logs.items():

        login_count = 0
        logout_count = 0

        usb_connect = 0
        usb_disconnect = 0

        http_visits = 0
        suspicious_http_visits = 0

        after_hours_events = 0

        devices = set()

        for event in events:

            cols = event.strip().split(",")

            if len(cols) < 6:
                continue

            event_type = cols[0].lower()
            timestamp = cols[2]
            pc_name = cols[4]
            action = cols[5].lower()

            devices.add(pc_name)

            # -----------------------------------
            # Login / Logout
            # -----------------------------------

            if event_type == "logon":

                if action == "logon":
                    login_count += 1

                elif action == "logoff":
                    logout_count += 1

            # -----------------------------------
            # USB
            # -----------------------------------

            elif event_type == "device":

                if action == "connect":
                    usb_connect += 1

                elif action == "disconnect":
                    usb_disconnect += 1

            # -----------------------------------
            # HTTP
            # -----------------------------------

            elif event_type == "http":

                http_visits += 1

                url = cols[5].lower()

                if any(keyword in url for keyword in SUSPICIOUS_KEYWORDS):
                    suspicious_http_visits += 1

            # -----------------------------------
            # After Office Hours
            # -----------------------------------

            try:

                dt = datetime.strptime(
                    timestamp,
                    "%m/%d/%Y %H:%M:%S"
                )

                hour = dt.hour

                if hour < 8 or hour >= 18:
                    after_hours_events += 1

            except Exception:
                pass

        employee_features.append({

            "employee": employee,

            "login_count": login_count,

            "logout_count": logout_count,

            "usb_connect": usb_connect,

            "usb_disconnect": usb_disconnect,

            "http_visits": http_visits,

            "suspicious_http_visits": suspicious_http_visits,

            "after_hours_events": after_hours_events,

            "unique_devices": len(devices),

            "total_events": len(events),

        })

    return pd.DataFrame(employee_features)


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    df = extract_features()

    print(df.head())

    df.to_csv(
        "ai_model/employee_features.csv",
        index=False,
    )

    print("\nFeatures extracted successfully.")

    print("Saved -> ai_model/employee_features.csv")