from pydantic import BaseModel
from typing import Optional


class DeptCreate(BaseModel):
    dept_name: str
    unit_id: int
    description: str
    org_id: int

class DeptUpdate(BaseModel):
    dept_name: Optional[str] = None
    unit_id: Optional[int] = None
    description: Optional[str] = None
    org_id: Optional[int] = None