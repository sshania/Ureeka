from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal
from models import Course 
from pydantic import BaseModel, Field

home_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class CourseResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

@home_router.get("/home/{student_id}", response_model=List[CourseResponse])
def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    courses = db.query(Course).filter(Course.student_id == student_id).all()
    if not courses:
        raise HTTPException(status_code=404, detail="Courses not found for this student")
    return courses