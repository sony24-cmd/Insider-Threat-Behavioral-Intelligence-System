from sqlalchemy.orm import Session

from models.activity_log import ActivityLog
from schemas.activity_log import (
    ActivityLogCreate,
    ActivityLogUpdate,
)


def create_activity_log(
    db: Session,
    activity: ActivityLogCreate,
):
    db_activity = ActivityLog(**activity.model_dump())

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    return db_activity


def get_activity_log(
    db: Session,
    activity_id: int,
):
    return (
        db.query(ActivityLog)
        .filter(ActivityLog.id == activity_id)
        .first()
    )


def get_all_activity_logs(db: Session):
    return db.query(ActivityLog).all()


def update_activity_log(
    db: Session,
    activity_id: int,
    activity: ActivityLogUpdate,
):
    db_activity = (
        db.query(ActivityLog)
        .filter(ActivityLog.id == activity_id)
        .first()
    )

    if not db_activity:
        return None

    update_data = activity.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(db_activity, key, value)

    db.commit()
    db.refresh(db_activity)

    return db_activity


def delete_activity_log(
    db: Session,
    activity_id: int,
):
    db_activity = (
        db.query(ActivityLog)
        .filter(ActivityLog.id == activity_id)
        .first()
    )

    if not db_activity:
        return None

    db.delete(db_activity)
    db.commit()

    return db_activity