from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas.behavior_profile import (
    BehaviorProfileCreate,
    BehaviorProfileUpdate,
    BehaviorProfileResponse,
)

from services.behavior_profile_service import (
    create_behavior_profile,
    get_all_behavior_profiles,
    get_behavior_profile,
    update_behavior_profile,
    delete_behavior_profile,
)

# NEW IMPORT
from services.behavior_analysis_service import (
    generate_behavior_profile,
)

router = APIRouter(
    prefix="/behavior-profiles",
    tags=["Behavior Profiles"],
)


# ==========================================
# Create Behavior Profile
# ==========================================

@router.post("/", response_model=BehaviorProfileResponse)
def create_profile(
    profile: BehaviorProfileCreate,
    db: Session = Depends(get_db),
):
    return create_behavior_profile(db, profile)


# ==========================================
# Get All Behavior Profiles
# ==========================================

@router.get("/", response_model=List[BehaviorProfileResponse])
def get_profiles(
    db: Session = Depends(get_db),
):
    return get_all_behavior_profiles(db)


# ==========================================
# Get Behavior Profile
# ==========================================

@router.get("/{profile_id}", response_model=BehaviorProfileResponse)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
):

    profile = get_behavior_profile(
        db,
        profile_id,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Behavior Profile not found",
        )

    return profile


# ==========================================
# Update Behavior Profile
# ==========================================

@router.put("/{profile_id}", response_model=BehaviorProfileResponse)
def update_profile(
    profile_id: int,
    profile: BehaviorProfileUpdate,
    db: Session = Depends(get_db),
):

    updated = update_behavior_profile(
        db,
        profile_id,
        profile,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Behavior Profile not found",
        )

    return updated


# ==========================================
# Delete Behavior Profile
# ==========================================

@router.delete("/{profile_id}")
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
):

    deleted = delete_behavior_profile(
        db,
        profile_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Behavior Profile not found",
        )

    return {
        "message": "Behavior Profile deleted successfully"
    }


# ==========================================
# Generate Behavior Profile Automatically
# ==========================================

@router.post("/generate/{employee_id}")
def generate_profile(
    employee_id: int,
    db: Session = Depends(get_db),
):

    profile = generate_behavior_profile(
        db,
        employee_id,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="No activity logs found for this employee.",
        )

    return profile