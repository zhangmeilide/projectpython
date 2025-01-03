from sqlalchemy import Column, Integer, String
from db import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True, index=True)
    org_id = Column(Integer,default=0)  # 可选字段

