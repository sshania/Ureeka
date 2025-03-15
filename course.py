from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
from models import Course
from pydantic import BaseModel
from typing import Optional

course_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CourseCreate(BaseModel):
    title: str
    description: str
    category_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    admin_id: int

class CourseUpdate(BaseModel):
    title: str
    description: str
    category_id: int
    updated_at: datetime
    admin_id: int

class CourseOut(BaseModel):
    course_id: int
    title: str
    description: str
    category_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    admin_id: int

    class Config:
        orm_mode: True        

# create
@course_router.post("/create/{admin_id}", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(
        title=course.title,
        description=course.description,
        category_id=course.category_id,
        created_at=course.created_at,
        updated_at=course.updated_at,
        admin_id=course.admin_id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

#list all course
@course_router.get("/", response_model=List[CourseOut])
def read_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

#detail course
@course_router.get("/detail/{course_id}", response_model=CourseOut)
def read_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# update course
@course_router.put("/update/{course_id}", response_model=CourseOut)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.course_id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_course.title = course.title
    db_course.description = course.description
    db_course.category_id = course.category_id
    db_course.updated_at = course.updated_at
    db_course.admin_id = course.admin_id
    
    db.commit()
    db.refresh(db_course)
    return db_course

#delete course
@course_router.delete("/delete/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.course_id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(db_course)
    db.commit()
    return {"message": "Course deleted successfully"}