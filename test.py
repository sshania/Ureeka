from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal
from models import Tests
from pydantic import BaseModel, Field

material_router = APIRouter()

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

