from fastapi import FastAPI
from db import engine
from routers import user

# 导入模型，确保数据库表被创建
from models import user as user_model
user_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 挂载用户模块路由
app.include_router(user.router, prefix="/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "欢迎使用用户管理 API 服务"}
