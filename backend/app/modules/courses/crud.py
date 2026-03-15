from sqlalchemy.orm import Session
from app.modules.courses.model import Course, Lesson, Word, Meaning
from app.modules.courses.schema import UpdateCourseParam

class CRUDCourse:
    @staticmethod
    def get(db: Session, course_id: str) -> Course | None:
        return db.query(Course).filter(Course.id == course_id).first()

    @staticmethod
    def get_list(db: Session, skip: int = 0, limit: int = 100) -> list[Course]:
        return db.query(Course).filter(Course.is_deleted == False).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, obj_in: dict) -> Course:
        db_obj = Course(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db: Session, db_obj: Course, obj_in: UpdateCourseParam) -> Course:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDLesson:
    @staticmethod
    def create(db: Session, obj_in: dict) -> Lesson:
        db_obj = Lesson(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

# Có thể thêm các CRUD khác cho Word/Meaning nếu cần logic phức tạp hơn
crud_course = CRUDCourse()
crud_lesson = CRUDLesson()
