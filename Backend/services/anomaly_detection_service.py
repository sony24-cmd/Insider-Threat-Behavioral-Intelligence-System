from sqlalchemy.orm import Session

from models.activity_log import ActivityLog


def extract_employee_features(
    db: Session,
    employee_id: int,
):
    """
    Extract employee behaviour features
    from activity logs.
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

        activity = log.activity_type.lower()

        if activity == "login":
            login_count += 1

        elif activity == "logout":
            logout_count += 1

        elif activity == "usb connected":
            usb_connect += 1

        elif activity == "usb disconnected":
            usb_disconnect += 1

        elif activity == "http visit":
            http_visits += 1

    return {
        "login_count": login_count,
        "logout_count": logout_count,
        "usb_connect": usb_connect,
        "usb_disconnect": usb_disconnect,
        "http_visits": http_visits,
        "total_events": len(logs),
    }