from datetime import datetime


# ==========================================
# Login Time Anomaly
# ==========================================

def detect_login_anomaly(profile, login_time: datetime):

    current_hour = login_time.hour + (login_time.minute / 60)

    difference = abs(current_hour - profile.avg_login_hour)

    if difference >= 2:
        return {
            "anomaly": True,
            "severity": "High",
            "reason": "Login time significantly differs from employee baseline."
        }

    elif difference >= 1:
        return {
            "anomaly": True,
            "severity": "Medium",
            "reason": "Login time slightly differs from employee baseline."
        }

    return {
        "anomaly": False,
        "severity": "Low",
        "reason": "Normal login pattern."
    }


# ==========================================
# After Hours Activity
# ==========================================

def detect_after_hours(login_time: datetime):

    if login_time.hour < 8 or login_time.hour > 18:
        return {
            "anomaly": True,
            "severity": "High",
            "reason": "Employee logged in outside office hours."
        }

    return {
        "anomaly": False,
        "severity": "Low",
        "reason": "Within office hours."
    }


# ==========================================
# Weekend Activity
# ==========================================

def detect_weekend_activity(login_time: datetime):

    if login_time.weekday() >= 5:
        return {
            "anomaly": True,
            "severity": "Medium",
            "reason": "Weekend activity detected."
        }

    return {
        "anomaly": False,
        "severity": "Low",
        "reason": "Weekday activity."
    }


# ==========================================
# USB Usage
# ==========================================

def detect_usb_anomaly(usb_count: int):

    if usb_count >= 5:
        return {
            "anomaly": True,
            "severity": "High",
            "reason": "Excessive USB connections."
        }

    elif usb_count >= 3:
        return {
            "anomaly": True,
            "severity": "Medium",
            "reason": "Frequent USB connections."
        }

    return {
        "anomaly": False,
        "severity": "Low",
        "reason": "Normal USB usage."
    }


# ==========================================
# Network Activity
# ==========================================

def detect_network_anomaly(http_visits: int):

    if http_visits >= 100:
        return {
            "anomaly": True,
            "severity": "High",
            "reason": "Unusually high network activity."
        }

    elif http_visits >= 60:
        return {
            "anomaly": True,
            "severity": "Medium",
            "reason": "Above-average network activity."
        }

    return {
        "anomaly": False,
        "severity": "Low",
        "reason": "Normal network usage."
    }