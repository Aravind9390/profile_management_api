# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.models.user import User as UserModel
from app.schemas import User as UserSchema, UserCreate as UserCreateSchema
from app.utils.enums import GenderEnum

router = APIRouter()

@router.post("/users/{gender}", response_model=UserSchema)
def create_user(user: UserCreateSchema, gender:GenderEnum,db: Session = Depends(database.get_db)):
    print(gender)
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = user.password + "notreallyhashed"  # Simulate password hashing
    db_user = UserModel(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
