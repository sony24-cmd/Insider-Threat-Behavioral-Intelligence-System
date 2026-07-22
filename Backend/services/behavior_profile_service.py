from sqlalchemy.orm import Session

from models.behavior_profile import BehaviorProfile

from schemas.behavior_profile import (
    BehaviorProfileCreate,
    BehaviorProfileUpdate,
)


# ==========================================
# Create Behavior Profile
# ==========================================

def create_behavior_profile(
    db: Session,
    profile: BehaviorProfileCreate,
):

    db_profile = BehaviorProfile(**profile.model_dump())

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return db_profile


# ==========================================
# Get All Behavior Profiles
# ==========================================

def get_all_behavior_profiles(
    db: Session,
):

    return db.query(BehaviorProfile).all()


# ==========================================
# Get Behavior Profile by Profile ID
# ==========================================

def get_behavior_profile(
    db: Session,
    profile_id: int,
):

    return (
        db.query(BehaviorProfile)
        .filter(
            BehaviorProfile.id == profile_id
        )
        .first()
    )


# ==========================================
# NEW
# Get Behavior Profile by Employee ID
# ==========================================

def get_behavior_profile_by_employee(
    db: Session,
    employee_id: int,
):

    return (
        db.query(BehaviorProfile)
        .filter(
            BehaviorProfile.employee_id == employee_id
        )
        .first()
    )


# ==========================================
# Update Behavior Profile
# ==========================================

def update_behavior_profile(
    db: Session,
    profile_id: int,
    profile: BehaviorProfileUpdate,
):

    db_profile = (
        db.query(BehaviorProfile)
        .filter(
            BehaviorProfile.id == profile_id
        )
        .first()
    )

    if not db_profile:
        return None

    for key, value in profile.model_dump(
        exclude_unset=True
    ).items():
        setattr(
            db_profile,
            key,
            value,
        )

    db.commit()
    db.refresh(db_profile)

    return db_profile


# ==========================================
# Delete Behavior Profile
# ==========================================

def delete_behavior_profile(
    db: Session,
    profile_id: int,
):

    db_profile = (
        db.query(BehaviorProfile)
        .filter(
            BehaviorProfile.id == profile_id
        )
        .first()
    )

    if not db_profile:
        return None

    db.delete(db_profile)
    db.commit()

    return db_profile