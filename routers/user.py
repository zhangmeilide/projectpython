from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from services.user_service import UserService, UserCreate

router = APIRouter()

# 获取数据库 session 的依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user)

@router.get("/")
async def get_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_all_users()

@router.get("/{username}")
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if "message" in user:
        raise HTTPException(status_code=404, detail=user["message"])
    return user
