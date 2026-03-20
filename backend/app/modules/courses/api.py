from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.deps import CurrentSession, CurrentAdmin, get_current_admin
from app.core.response import response_base, ResponseModel
from app.modules.courses.schema import (
    GetCourseDetail, CreateCourseParam, UpdateCourseParam, 
    GetLessonDetail, CreateLessonParam,
    GetWordDetail, GetMeaningDetail,
    BulkImportCourseParam
)
from app.modules.courses.crud import crud_course, crud_lesson
from app.modules.courses.model import Course, Lesson, Word, Meaning
from datetime import datetime

router = APIRouter()

# --- USER APIs ---

@router.get("/", summary="Lấy danh sách khóa học cho User")
def get_courses(
    db: CurrentSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1)
) -> ResponseModel[List[GetCourseDetail]]:
    courses = crud_course.get_list(db, skip=skip, limit=limit)
    return response_base.success(data=courses)

@router.get("/{course_id}", summary="Lấy chi tiết khóa học (bao gồm lesson, word)")
def get_course_detail(db: CurrentSession, course_id: str) -> ResponseModel[GetCourseDetail]:
    course = crud_course.get(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return response_base.success(data=course)

# --- ADMIN APIs ---

@router.post("/", summary="[Admin] Tạo khóa học mới", dependencies=[Depends(get_current_admin)])
def create_course(db: CurrentSession, obj_in: CreateCourseParam) -> ResponseModel[GetCourseDetail]:
    course = crud_course.create(db, obj_in.model_dump())
    return response_base.success(data=course, msg="Tạo khóa học thành công")

@router.put("/{course_id}", summary="[Admin] Cập nhật khóa học", dependencies=[Depends(get_current_admin)])
def update_course(
    db: CurrentSession, 
    course_id: str, 
    obj_in: UpdateCourseParam
) -> ResponseModel[GetCourseDetail]:
    db_obj = crud_course.get(db, course_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Course not found")
    course = crud_course.update(db, db_obj, obj_in)
    return response_base.success(data=course, msg="Cập nhật thành công")

@router.post("/{course_id}/lessons", summary="[Admin] Thêm bài học vào khóa học", dependencies=[Depends(get_current_admin)])
def create_lesson(
    db: CurrentSession, 
    course_id: str, 
    obj_in: CreateLessonParam
) -> ResponseModel[GetLessonDetail]:
    lesson_data = obj_in.model_dump()
    lesson_data["course_id"] = course_id
    lesson = crud_lesson.create(db, lesson_data)
    return response_base.success(data=lesson, msg="Thêm bài học thành công")

@router.post("/import", summary="[Admin] Import hàng loạt khóa học", dependencies=[Depends(get_current_admin)])
def import_courses(db: CurrentSession, courses_in: List[BulkImportCourseParam]) -> ResponseModel:
    for course_data in courses_in:
        # 1. Tạo Course
        course_dict = course_data.model_dump(exclude={"lessons"})
        db_course = Course(**course_dict)
        db.add(db_course)
        db.flush()

        for lesson_data in course_data.lessons:
            # 2. Tạo Lesson
            lesson_dict = lesson_data.model_dump(exclude={"words"})
            lesson_dict["course_id"] = db_course.id
            db_lesson = Lesson(**lesson_dict)
            db.add(db_lesson)
            db.flush()

            for word_data in lesson_data.words:
                # 3. Tạo Word
                word_dict = word_data.model_dump(exclude={"meanings"})
                word_dict["lesson_id"] = db_lesson.id
                db_word = Word(**word_dict)
                db.add(db_word)
                db.flush()

                for meaning_data in word_data.meanings:
                    # 4. Tạo Meaning
                    meaning_dict = meaning_data.model_dump()
                    meaning_dict["word_id"] = db_word.id
                    db_meaning = Meaning(**meaning_dict)
                    db.add(db_meaning)
    
    db.commit()
    return response_base.success(msg=f"Đã import thành công {len(courses_in)} khóa học")
