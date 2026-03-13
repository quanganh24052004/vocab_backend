import json
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.modules.courses.model import Course, Lesson, Word, Meaning

def seed_data():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        old_courses = db.query(Course).all()
        if old_courses:
            print("Đang xoá dữ liệu cũ...")
            for c in old_courses:
                db.delete(c)
            db.commit()

        json_path = os.getenv("JSON_DATA_PATH", ".test/courses_data.json")
        if not os.path.exists(json_path):
            print(f"Lỗi: Không tìm thấy file {json_path}")
            return
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for course_data in data:
            course = Course(
                name=course_data.get("name"),
                description=course_data.get("description"),
                sub_description=course_data.get("subDescription")
            )
            db.add(course)
            db.flush()

            for lesson_data in course_data.get("lessons", []):
                lesson = Lesson(
                    course_id=course.id,
                    name=lesson_data.get("name"),
                    sub_name=lesson_data.get("subName"),
                    quantity_of_word=lesson_data.get("quantityOfWord", 0)
                )
                db.add(lesson)
                db.flush()

                for word_data in lesson_data.get("words", []):
                    word = Word(
                        lesson_id=lesson.id,
                        english=word_data.get("english"),
                        phonetic=word_data.get("phonetic"),
                        part_of_speech=word_data.get("partOfSpeech"),
                        audio_url=word_data.get("audioUrl"),
                        cefr=word_data.get("CEFR")
                    )
                    db.add(word)
                    db.flush()

                    for meaning_data in word_data.get("meanings", []):
                        meaning = Meaning(
                            word_id=word.id,
                            vietnamese=meaning_data.get("vietnamese"),
                            example_en=meaning_data.get("exampleEn"),
                            example_vi=meaning_data.get("exampleVi")
                        )
                        db.add(meaning)
        db.commit()
        print("Import thành công!")
    except Exception as e:
        print(f"Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
