from sqlalchemy.orm import Session
from app.modules.users.model import User
from app.modules.users.schema import UpdateUserParam

class CRUDUser:
    @staticmethod
    def get(db: Session, user_id: str) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, db_obj: User, obj_in: UpdateUserParam) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, user_id: str) -> bool:
        db_obj = db.query(User).filter(User.id == user_id).first()
        if not db_obj:
            return False
        db.delete(db_obj)
        db.commit()
        return True

crud_user = CRUDUser()
