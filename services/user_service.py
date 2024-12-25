from sqlalchemy.orm import Session
from models.user import User
from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    name: str
    mobile: str

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> dict:
        db_user = User(name=user.name, email=user.mobile)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return {"message": "用户创建成功", "user": db_user}

    def get_all_users(self) -> List[dict]:
        users = self.db.query(User).all()
        return [{"id": user.id, "name": user.name, "mobile": user.mobile} for user in users]

    def get_user_by_username(self, name: str) -> dict:
        print(1)
        exit()
        user = self.db.query(User).filter(User.name == name).first()
        if user:
            return {"id": user.id, "mibile": user.mibile, "name": user.name}
        return {"message": f"用户 {name} 不存在"}
