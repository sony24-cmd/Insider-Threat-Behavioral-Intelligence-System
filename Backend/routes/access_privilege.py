from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas.access_privilege import (
    AccessPrivilegeCreate,
    AccessPrivilegeUpdate,
    AccessPrivilegeResponse,
)

from services import access_privilege_service

router = APIRouter(
    prefix="/access",
    tags=["Access Privileges"],
)


@router.post("/", response_model=AccessPrivilegeResponse)
def create_access(
    access: AccessPrivilegeCreate,
    db: Session = Depends(get_db),
):
    return access_privilege_service.create_access(db, access)


@router.get("/", response_model=list[AccessPrivilegeResponse])
def get_all_access(db: Session = Depends(get_db)):
    return access_privilege_service.get_all_access(db)


@router.get("/{access_id}", response_model=AccessPrivilegeResponse)
def get_access(access_id: int, db: Session = Depends(get_db)):
    access = access_privilege_service.get_access(db, access_id)

    if access is None:
        raise HTTPException(
            status_code=404,
            detail="Access Privilege not found",
        )

    return access


@router.put("/{access_id}", response_model=AccessPrivilegeResponse)
def update_access(
    access_id: int,
    access: AccessPrivilegeUpdate,
    db: Session = Depends(get_db),
):
    updated = access_privilege_service.update_access(
        db,
        access_id,
        access,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Access Privilege not found",
        )

    return updated


@router.delete("/{access_id}")
def delete_access(
    access_id: int,
    db: Session = Depends(get_db),
):
    deleted = access_privilege_service.delete_access(
        db,
        access_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Access Privilege not found",
        )

    return {
        "message": "Access Privilege deleted successfully"
    }