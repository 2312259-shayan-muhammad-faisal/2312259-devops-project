from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from . import models, database
from pydantic import BaseModel

app = FastAPI(title="DevOps Project - 2312259")


@app.on_event("startup")
def on_startup():
    try:
        models.Base.metadata.create_all(bind=database.engine)
    except Exception:
        pass  # In tests, the test DB handles table creation


class StudentCreate(BaseModel):
    reg_no: str
    name: str
    email: str


class StudentResponse(StudentCreate):
    id: int

    class Config:
        from_attributes = True


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return {
        "status": "ok",
        "db": db_status,
        "student": "2312259"
    }


@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(
        models.Student.reg_no == student.reg_no
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student with this reg_no already exists.")
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@app.get("/students/{reg_no}", response_model=StudentResponse)
def get_student(reg_no: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.reg_no == reg_no
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
