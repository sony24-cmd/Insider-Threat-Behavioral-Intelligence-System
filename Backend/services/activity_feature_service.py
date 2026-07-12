from sqlalchemy.orm import Session
from models.activity_log import ActivityLog


def extract_employee_features(
    db: Session,
    employee_id: int,
):
    """
    Extract behavioural features for an employee
    from all activity logs.
    """

    logs = (
        db.query(ActivityLog)
        .filter(ActivityLog.employee_id == employee_id)
        .all()
    )

    login_count = 0
    logout_count = 0
    usb_connect = 0
    usb_disconnect = 0
    http_visits = 0

    for log in logs:

        activity = (log.activity_type or "").upper()

        if activity == "LOGIN":
            login_count += 1

        elif activity == "LOGOUT":
            logout_count += 1

        elif activity == "USB_CONNECT":
            usb_connect += 1

        elif activity == "USB_DISCONNECT":
            usb_disconnect += 1

        elif activity in [
            "HTTP",
            "WEB",
            "WEB_ACCESS",
            "HTTP_VISIT",
        ]:
            http_visits += 1

    return {
        "login_count": login_count,
        "logout_count": logout_count,
        "usb_connect": usb_connect,
        "usb_disconnect": usb_disconnect,
        "http_visits": http_visits,
        "total_events": len(logs),
    }