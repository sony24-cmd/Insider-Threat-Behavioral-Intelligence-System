from sqlalchemy.orm import Session

from models.user import User
from schemas.user_schema import UserRegister
from utils.jwt_handler import create_access_token
from utils.password import hash_password, verify_password


class AuthService:
    @staticmethod
    def register_user(db: Session, user: UserRegister):
        """
        Register a new user.
        """

        existing_user = (
            db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_user:
            return None

        new_user = User(
            name=user.name,
            email=user.email,
            password=hash_password(user.password),
            role=user.role,
            department=user.department,
            designation=user.designation,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def login_user(db: Session, email: str, password: str):
        """
        Authenticate user and return a JWT token.
        """

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        access_token = create_access_token(
            {
                "sub": user.email,
                "user_id": user.id,
                "role": user.role,
            }
        )

        return access_token