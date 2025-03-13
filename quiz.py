from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal
from models import Tests, Questions, Answers
from pydantic import BaseModel, Field

quiz_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TestCreate(BaseModel):
    course_id: int = Field(..., description="Course ID harus ada")
    test_id: int
    title: str
    description: str
    pass_percentage: int
    time_limit: int
    admin_id: int = Field(..., description="Login as Admin to create test")

class TestUpdate(BaseModel):
    course_id: int
    test_id: int
    title: str
    description: str
    pass_percentage: int
    time_limit: int
    admin_id: int

class TestOut(BaseModel):
    test_id: int
    course_id: int
    title: str
    description: str
    pass_percentage: int
    time_limit: int
    admin_id: int

    class Config:
        orm_mode: True

class QuestionCreate(BaseModel):
    test_id: int = Field(..., description="Test ID harus ada")
    question_id: int
    question: str
    question_type: str
    marks: int
    admin_id: int = Field(..., description="Login as Admin to create question")

class QuestionUpdate(BaseModel):
    test_id: int
    question_id: int
    question: str
    question_type: str
    marks: int
    admin_id: int

class QuestionOut(BaseModel):
    question_id: int
    test_id: int
    question: str
    question_type: str
    marks: int
    admin_id: int

    class Config:
        orm_mode: True

class AnswerCreate(BaseModel):
    question_id: int = Field(..., description="Question ID harus ada")
    answer_id: int
    answer: str
    is_correct: bool
    admin_id: int = Field(..., description="Login as Admin to create answer")

class AnswerUpdate(BaseModel):
    question_id: int
    answer_id: int
    answer: str
    is_correct: bool
    admin_id: int

class AnswerOut(BaseModel):
    answer_id: int
    question_id: int
    answer: str
    is_correct: bool
    admin_id: int

    class Config:
        orm_mode: True 

@quiz_router.post("/test/create", response_model=TestOut)
def create_test(test: TestCreate, db: Session = Depends(get_db)):
    new_test = Tests(course_id=test.course_id, test_id=test.test_id, title=test.title, description=test.description, pass_percentage=test.pass_percentage, time_limit=test.time_limit, admin_id=test.admin_id)
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test

@quiz_router.get("/test/{test_id}", response_model=TestOut)
def get_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(Tests).filter(Tests.test_id == test_id).first()
    if test is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
    return test

@quiz_router.put("/test/update/{test_id}", response_model=TestOut)
def update_test(test_id: int, test: TestUpdate, db: Session = Depends(get_db)):
    db_test = db.query(Tests).filter(Tests.test_id == test_id).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    db_test.course_id = test.course_id
    db_test.title = test.title
    db_test.description = test.description
    db_test.pass_percentage = test.pass_percentage
    db_test.time_limit = test.time_limit
    db_test.admin_id = test.admin_id
    
    db.commit()
    db.refresh(db_test)
    return db_test

@quiz_router.delete("/test/delete/{test_id}", response_model=TestOut)
def delete_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(Tests).filter(Tests.test_id == test_id).first()
    if test is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
    db.delete(test)
    db.commit()
    return test

@quiz_router.post("/question/create/{test_id}", response_model=QuestionOut)
def create_question(test_id: int, question: QuestionCreate, db: Session = Depends(get_db)):
    new_question = Questions(test_id=question.test_id, question_id=question.question_id, question=question.question, question_type=question.question_type, marks=question.marks, admin_id=question.admin_id)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

@quiz_router.get("/question/{test_id}/{question_id}", response_model=QuestionOut)
def get_question(test_id: int, question_id: int, db: Session = Depends(get_db)):
    question = db.query(Questions).filter(Questions.test_id == test_id, Questions.question_id == question_id).first()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question

@quiz_router.put("/question/update/{test_id}/{question_id}", response_model=QuestionOut)
def update_question(question_id: int, question: QuestionUpdate, db: Session = Depends(get_db)):
    db_question = db.query(Questions).filter(Questions.question_id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db_question.test_id = question.test_id
    db_question.text = question.text
    db.commit()
    db.refresh(db_question)
    return db_question

@quiz_router.delete("/question/delete/{test_id}/{question_id}", response_model=QuestionOut)
def delete_question(test_id: int, question_id: int, db: Session = Depends(get_db)):
    question = db.query(Questions).filter(Questions.test_id == test_id, Questions.question_id == question_id).first()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    db.delete(question)
    db.commit()
    return question

@quiz_router.post("/answer/create/{test_id}/{question_id}", response_model=AnswerOut)
def create_answer(test_id: int, question_id: int, answer: AnswerCreate, db: Session = Depends(get_db)):
    new_answer = Answers(question_id=answer.question_id, answer_id=answer.answer_id, answer=answer.answer, is_correct=answer.is_correct, admin_id=answer.admin_id)
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer

@quiz_router.get("/answer/{test_id}/{question_id}/{answer_id}", response_model=AnswerOut)
def get_answer(test_id: int, question_id: int, answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(Answers).filter(Answers.question_id == question_id, Answers.answer_id == answer_id).first()
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
    return answer

@quiz_router.put("/answer/update/{test_id}/{question_id}/{answer_id}", response_model=AnswerOut)
def update_answer(answer_id: int, answer: AnswerUpdate, db: Session = Depends(get_db)):
    db_answer = db.query(Answers).filter(Answers.answer_id == answer_id).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    db_answer.question_id = answer.question_id
    db_answer.text = answer.text
    db_answer.is_correct = answer.is_correct
    
    db.commit()
    db.refresh(db_answer)
    return db_answer

@quiz_router.delete("/answer/delete/{test_id}/{question_id}/{answer_id}", response_model=AnswerOut)
def delete_answer(test_id: int, question_id: int, answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(Answers).filter(Answers.question_id == question_id, Answers.answer_id == answer_id).first()
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
    db.delete(answer)
    db.commit()
    return answer

@quiz_router.get("/answers/{test_id}/{question_id}", response_model=List[AnswerOut])
def get_answers(test_id: int, question_id: int, db: Session = Depends(get_db)):
    answers = db.query(Answers).filter(Answers.question_id == question_id).all()
    return answers