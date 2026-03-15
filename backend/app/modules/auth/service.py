from sqlalchemy.orm import Session
from app.core import security
from app.modules.auth.crud import crud_user
from app.modules.auth.schema import RegisterParam, AuthParam
from app.modules.users.model import User
from app.core.conf import settings

class AuthService:
    @staticmethod
    def register(db: Session, obj_in: RegisterParam) -> User:
        hashed_password = security.get_password_hash(obj_in.password)
        user_data = {
            "email": obj_in.email,
            "hashed_password": hashed_password,
            "name": obj_in.name,
            "role": "admin" if obj_in.email == settings.ADMIN_EMAIL else "user"
        }
        return crud_user.create(db, user_data)

    @staticmethod
    def authenticate(db: Session, obj_in: AuthParam) -> User | None:
        user = crud_user.get_by_email(db, obj_in.username)
        if not user:
            return None
        if not security.verify_password(obj_in.password, user.hashed_password):
            return None
        return user

auth_service = AuthService()
