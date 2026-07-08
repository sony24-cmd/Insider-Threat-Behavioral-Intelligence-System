from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from dependencies.roles import require_role


router = APIRouter(
    prefix="/admin",
    tags=["Administrator"]
)


# ---------------------------------
# View All Users
# Only Administrator allowed
# ---------------------------------

@router.get(
    "/users"
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("Administrator")
    )
):

    users = db.query(User).all()

    # Remove password before sending response
    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "department": user.department,
            "designation": user.designation,
            "created_at": user.created_at
        }
        for user in users
    ]



# ---------------------------------
# Delete User
# Only Administrator allowed
# ---------------------------------

@router.delete(
    "/users/{user_id}"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("Administrator")
    )
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    db.delete(user)
    db.commit()


    return {
        "message": "User deleted successfully"
    }



# ---------------------------------
# Change User Role
# Only Administrator allowed
# ---------------------------------

@router.put(
    "/users/{user_id}/role"
)
def update_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("Administrator")
    )
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    allowed_roles = [
        "Administrator",
        "Security Manager",
        "Security Analyst",
        "SOC Engineer"
    ]


    if role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )


    user.role = role

    db.commit()
    db.refresh(user)


    return {
        "message": "Role updated successfully",
        "new_role": user.role
    }