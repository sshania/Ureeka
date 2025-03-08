from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal
from models import Materials, Course
from pydantic import BaseModel, Field

material_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MaterialCreate(BaseModel):
    course_id: int = Field(..., description="Course ID harus ada")
    title: str
    description: str
    material_type: str
    upload_at: datetime
    admin_id: int

class MaterialUpdate(BaseModel):
    course_id: int
    title: str
    description: str
    material_type: str
    upload_at: datetime
    admin_id: int

class MaterialOut(BaseModel):
    material_id: int
    course_id: int
    title: str
    description: str
    material_type: str
    upload_at: datetime
    admin_id: int

    class Config:
        orm_mode: True

@material_router.post("/create/{course_id}", response_model=MaterialOut, status_code=status.HTTP_201_CREATED)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):

    course = db.query(Courses).filter(Courses.course_id == material.course_id).first()
    if not course:
        raise HTTPException(status_code=400, detail="Course ID tidak ditemukan")
    
    new_material = Materials(
        course_id=material.course_id,
        title=material.title,
        description=material.description,
        material_type=material.material_type,
        upload_at=material.upload_at,
        admin_id=material.admin_id
    )
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material


@material_router.get("/", response_model=List[MaterialOut])
def read_materials(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    materials = db.query(Materials).offset(skip).limit(limit).all()
    return materials

#detail
@material_router.get("/detail/{material_id}", response_model=MaterialOut)
def read_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Materials).filter(Materials.material_id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@material_router.put("/update/{material_id}", response_model=MaterialOut)
def update_material(material_id: int, material: MaterialUpdate, db: Session = Depends(get_db)):
    db_material = db.query(Materials).filter(Materials.material_id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    
    db_material.course_id = material.course_id
    db_material.title = material.title
    db_material.description = material.description
    db_material.material_type = material.material_type
    db_material.upload_at = material.upload_at
    db_material.admin_id = material.admin_id
    
    db.commit()
    db.refresh(db_material)
    return db_material

@material_router.delete("/delete/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(material_id: int, db: Session = Depends(get_db)):
    db_material = db.query(Materials).filter(Materials.material_id == material_id).first()
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    
    db.delete(db_material)
    db.commit()
    return {"message": "Material deleted successfully"}