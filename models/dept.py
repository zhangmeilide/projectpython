from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dept(Base):
    __tablename__ = 'tb_dept'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name = Column(String(100), nullable=False, default='')
    unit_id = Column(Integer, nullable=False, default=0)
    description = Column(String(255), nullable=False, default='')
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    org_id = Column(Integer, default=0)