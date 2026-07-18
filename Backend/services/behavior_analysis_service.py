from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.activity_log import ActivityLog
from models.behavior_profile import BehaviorProfile


# ==========================================
# Generate Behavior Baseline
# ==========================================

def generate_behavior_profile(
    db: Session,
    employee_id: int,
):
    """
    Analyze an employee's activity logs and
    generate/update the behavior profile.
    """

    logs = (
        db.query(ActivityLog)
        .filter(ActivityLog.employee_id == employee_id)
        .all()
    )

    if not logs:
        return None

    login_hours = []
    logout_hours = []

    usb_count = 0
    file_count = 0
    network_count = 0
    device_switches = 0

    login_events = 0

    for log in logs:

        activity = log.activity_type.lower()

        if activity == "login":
            login_events += 1
            login_hours.append(
                log.timestamp.hour +
                log.timestamp.minute / 60
            )

        elif activity == "logout":
            logout_hours.append(
                log.timestamp.hour +
                log.timestamp.minute / 60
            )

        elif "usb" in activity:
            usb_count += 1

        elif "file" in activity:
            file_count += 1

        elif "network" in activity:
            network_count += 1

        elif "device" in activity:
            device_switches += 1

    avg_login = (
        sum(login_hours) / len(login_hours)
        if login_hours else 9.0
    )

    avg_logout = (
        sum(logout_hours) / len(logout_hours)
        if logout_hours else 18.0
    )

    profile = (
        db.query(BehaviorProfile)
        .filter(
            BehaviorProfile.employee_id == employee_id
        )
        .first()
    )

    if profile:

        profile.avg_login_hour = avg_login
        profile.avg_logout_hour = avg_logout
        profile.avg_daily_logins = login_events
        profile.avg_usb_usage = usb_count
        profile.avg_file_access = file_count
        profile.avg_network_usage = network_count
        profile.avg_device_switches = device_switches
        profile.last_updated = datetime.utcnow()

    else:

        profile = BehaviorProfile(

            employee_id=employee_id,

            avg_login_hour=avg_login,

            avg_logout_hour=avg_logout,

            avg_daily_logins=login_events,

            avg_file_access=file_count,

            avg_usb_usage=usb_count,

            avg_network_usage=network_count,

            avg_device_switches=device_switches,

            baseline_risk="Low",
        )

        db.add(profile)

    db.commit()
    db.refresh(profile)

    return profile