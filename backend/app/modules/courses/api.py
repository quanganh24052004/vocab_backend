from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.deps import CurrentSession, CurrentAdmin
from app.core.response import response_base, ResponseModel
from app.modules.courses.schema import (
    GetCourseDetail, CreateCourseParam, UpdateCourseParam, 
    GetLessonDetail, CreateLessonParam,
    GetWordDetail, GetMeaningDetail
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

@router.post("/", summary="[Admin] Tạo khóa học mới", dependencies=[Depends(CurrentAdmin)])
def create_course(db: CurrentSession, obj_in: CreateCourseParam) -> ResponseModel[GetCourseDetail]:
    course = crud_course.create(db, obj_in.model_dump())
    return response_base.success(data=course, msg="Tạo khóa học thành công")

@router.put("/{course_id}", summary="[Admin] Cập nhật khóa học", dependencies=[Depends(CurrentAdmin)])
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

@router.post("/{course_id}/lessons", summary="[Admin] Thêm bài học vào khóa học", dependencies=[Depends(CurrentAdmin)])
def create_lesson(
    db: CurrentSession, 
    course_id: str, 
    obj_in: CreateLessonParam
) -> ResponseModel[GetLessonDetail]:
    lesson_data = obj_in.model_dump()
    lesson_data["course_id"] = course_id
    lesson = crud_lesson.create(db, lesson_data)
    return response_base.success(data=lesson, msg="Thêm bài học thành công")
