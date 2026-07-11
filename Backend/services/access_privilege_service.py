from sqlalchemy.orm import Session

from models.access_privilege import AccessPrivilege
from schemas.access_privilege import (
    AccessPrivilegeCreate,
    AccessPrivilegeUpdate,
)


def create_access(db: Session, access: AccessPrivilegeCreate):
    db_access = AccessPrivilege(**access.model_dump())

    db.add(db_access)
    db.commit()
    db.refresh(db_access)

    return db_access


def get_all_access(db: Session):
    return db.query(AccessPrivilege).all()


def get_access(db: Session, access_id: int):
    return (
        db.query(AccessPrivilege)
        .filter(AccessPrivilege.id == access_id)
        .first()
    )


def update_access(
    db: Session,
    access_id: int,
    access: AccessPrivilegeUpdate,
):
    db_access = (
        db.query(AccessPrivilege)
        .filter(AccessPrivilege.id == access_id)
        .first()
    )

    if not db_access:
        return None

    update_data = access.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_access, key, value)

    db.commit()
    db.refresh(db_access)

    return db_access


def delete_access(db: Session, access_id: int):
    db_access = (
        db.query(AccessPrivilege)
        .filter(AccessPrivilege.id == access_id)
        .first()
    )

    if not db_access:
        return None

    db.delete(db_access)
    db.commit()

    return db_access