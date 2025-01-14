from fastapi import FastAPI
from db import engine
from routers import user,company,clue,file_router

# 导入模型，确保数据库表被创建
from models import user as user_model
user_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 挂载用户模块路由
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(company.router, prefix="/companys", tags=["Companys"])
app.include_router(clue.router, prefix="/clues", tags=["Clues"])
# 注册文件路由
app.include_router(file_router.router, prefix="/files", tags=["文件管理"])

@app.get("/")
async def root():
    return {"message": "欢迎使用网络交易监管系统 API 服务"}
