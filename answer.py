from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal
from models import Answers, Materials
from pydantic import BaseModel

answer_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AnswerCreate(BaseModel):
    answer_id: int
    question_id: int
    answer_text: str
    is_correct: bool
    explanation: str

class AnswerUpdate(BaseModel):
    answer_id: int
    question_id: int
    answer_text: str
    is_correct: bool
    explanation: str

class AnswerOut(BaseModel):
    answer_id: int 
    question_id: int
    answer_text: str
    is_correct: bool
    explanation: str

    class Config:
        orm_mode: True

@answer_router.post("/create/", response_model=AnswerOut, status_code=status.HTTP_201_CREATED)
def create_answer(answer: AnswerCreate, db: Session = Depends(get_db)):
    new_answer = Answers(
        answer_id=answer.answer_id,
        question_id=answer.question_id,
        answer_text=answer.answer_text,
        is_correct=answer.is_correct,
        explanation=answer.explanation
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer

@answer_router.get("/", response_model=List[AnswerOut])
def read_answers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    answers = db.query(answers).offset(skip).limit(limit).all()
    return answers

@answer_router.get("/detail/{answer_id}", response_model=AnswerOut)
def read_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(Answers).filter(Answers.answer_id == answer_id).first()
    if answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer

@answer_router.put("/update/{answer_id}", response_model=AnswerOut)
def update_answer(answer_id: int, answer: AnswerUpdate, db: Session = Depends(get_db)):
    db_answer = db.query(Answers).filter(Answers.answer_id == answer_id).first()
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    db_answer.answer_text = answer.answer_text
    db_answer.is_correct = answer.is_correct
    db_answer.explanation = answer.explanation
    db.commit()
    db.refresh(db_answer)
    return db_answer

@answer_router.delete("/delete/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    db_answer = db.query(Answers).filter(Answers.answer_id == answer_id).first()
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    db.delete(db_answer)
    db.commit()
    return {"message": "Answer deleted successfully"}