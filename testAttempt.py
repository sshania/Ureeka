from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal
from models import Answers, Tests_Attempts, Student_Answers, Tests
from pydantic import BaseModel, Field

testAttempt_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TestAttemptCreate(BaseModel):
    test_id: int = Field(..., description="Test ID harus ada")
    student_id: int = Field(..., description="Student ID harus ada")
    started_at: datetime
    completed_at: datetime
    score: int
    passed: bool
    total_time: int

class TestAttemptUpdate(BaseModel):
    test_id: int
    student_id: int
    started_at: datetime
    completed_at: datetime
    score: int
    passed: bool
    total_time: int

class TestAttemptOut(BaseModel):
    attempt_id: int
    test_id: int
    student_id: int
    started_at: datetime
    completed_at: datetime
    score: int
    passed: bool
    total_time: int

    class Config:
        orm_mode: True

@testAttempt_router.post("/attempt/create/{student_id}/{test_id}", response_model=TestAttemptOut)
def create_attempt(student_id: int, test_id: int, attempt: TestAttemptCreate, db: Session = Depends(get_db)):
    if student_id != attempt.student_id or test_id != attempt.test_id:
        raise HTTPException(status_code=400, detail="Mismatch between URL and request body")
    
    new_attempt = Tests_Attempts(**attempt.dict())
    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)
    
    return calculate_score(new_attempt.attempt_id, db)

@testAttempt_router.post("/attempt/calculate_score/{student_id}/{test_id}/{attempt_id}", response_model=TestAttemptOut)
def calculate_score(attempt_id: int, db: Session = Depends(get_db)):
    attempt = db.query(Tests_Attempts).filter_by(attempt_id=attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    student_answers = db.query(Student_Answers).filter_by(
        student_id=attempt.student_id, test_id=attempt.test_id
    ).all()
    
    if not student_answers:
        raise HTTPException(status_code=400, detail="No answers found for this attempt")
    
    correct_count = sum(
        1 for ans in student_answers if db.query(Answers)
        .filter_by(question_id=ans.question_id, is_correct=True, answer_id=ans.answer_id)
        .first()
    )
    
    total_questions = len(student_answers)
    attempt.score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    attempt.passed = attempt.score >= 60
    
    db.commit()
    db.refresh(attempt)
    return attempt



@testAttempt_router.get("/attempt/{student_id}/{test_id}/{attempt_id}", response_model=TestAttemptOut)
def get_attempt(attempt_id: int, db: Session = Depends(get_db)):
    attempt = db.query(Tests_Attempts).filter_by(attempt_id=attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt

@testAttempt_router.put("/attempt/update/{student_id}/{test_id}/{attempt_id}", response_model=TestAttemptOut)
def update_attempt(attempt_id: int, attempt_update: TestAttemptUpdate, db: Session = Depends(get_db)):
    attempt = db.query(Tests_Attempts).filter_by(attempt_id=attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    for key, value in attempt_update.dict().items():
        setattr(attempt, key, value)
    
    db.commit()
    db.refresh(attempt)
    return attempt

@testAttempt_router.delete("/attempt/delete/{student_id}/{test_id}/{attempt_id}", response_model=TestAttemptOut)
def delete_attempt(attempt_id: int, db: Session = Depends(get_db)):
    attempt = db.query(Tests_Attempts).filter_by(attempt_id=attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    db.delete(attempt)
    db.commit()
    return attempt

@testAttempt_router.get("/attempts/{student_id}/{test_id}", response_model=List[TestAttemptOut])
def get_attempts(student_id: int, test_id: int, db: Session = Depends(get_db)):
    return db.query(Tests_Attempts).filter_by(student_id=student_id, test_id=test_id).all()


