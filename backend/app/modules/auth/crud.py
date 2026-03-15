from sqlalchemy.orm import Session
from app.modules.users.model import User

class CRUDUser:
    @staticmethod
    def get_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, obj_in: dict) -> User:
        db_obj = User(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_user = CRUDUser()
