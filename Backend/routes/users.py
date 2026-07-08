from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user
from models.user import User
from schemas.user_schema import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/profile",
    response_model=UserResponse
)
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user