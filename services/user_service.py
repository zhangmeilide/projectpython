from sqlalchemy.orm import Session
from models.user import User
from pydantic import BaseModel
from typing import List,Optional

class UserCreate(BaseModel):
    name: str
    mobile: str
    org_id: Optional[int] = 0
    password:str

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> dict:
        print(f"{user}")
        db_user = User(name=user.name, mobile=user.mobile,org_id=user.org_id,password=user.password)
        print(f"{db_user}")
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return {"message": "用户创建成功", "user": db_user}

    def get_all_users(self) -> List[dict]:
        users = self.db.query(User).all()
        return [{"id": user.id, "name": user.name, "mobile": user.mobile} for user in users]

    def get_user_info(self, mobile: str) -> dict:
        # print(f"{name}")
        user = self.db.query(User).filter(User.mobile == mobile).first()
        if user:
            return {"id": user.id, "mobile": user.mobile, "name": user.name,"password":user.password}
        return {"message": f"用户 {mobile} 不存在"}

    def get_user_by_username(self, name: str) -> dict:
        user = self.db.query(User).filter(User.mobile == name).first()
        if user:
            # 提取返回的字段，换行写更易读
            user_data = {
                "id": user.id,
                "mobile": user.mobile,
                "name": user.name,
                "org_id": user.org_id,
                "dept_id": user.dept_id,
                "duty": user.duty,
                "app_id": user.app_id,
            }
            return user_data
        return {"message": f"用户 {name} 不存在"}