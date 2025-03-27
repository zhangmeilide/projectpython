from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session

# 数据库 URL（假设使用 MySQL）
#DATABASE_URL = "mysql://root:yhblsqtxswl2021@121.89.172.70/wjxt_sx"  # 替换为你自己的 MySQL 配置信息
# 数据库 URL（假设使用 PyMySQL 作为驱动）
DATABASE_URL = "mysql+pymysql://root:yhblsqtxswl2021@121.89.172.70/wjxt_sx"  # 替换为你自己的 MySQL

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)

# 创建 SessionLocal 类，用于生成会话对象
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础类，用于所有数据库模型的继承
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()