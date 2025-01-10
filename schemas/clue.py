from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClueCreate(BaseModel):
    clue_name: str
    clue_url: str
    company_id: int
    company_name: str
    org_id: int
    dept_id: int
    work_source_flag:int
    clue_behavior_id: Optional[int] = 0

class ClueUpdate(BaseModel):
    clue_name: Optional[str] = ""
    clue_url: Optional[str] = ""
    company_id: Optional[int] = 0
    company_name: Optional[str] = ""
    org_id: Optional[int] = 0
    dept_id: Optional[int] = 0
    work_source_flag: Optional[int] = 1
    clue_behavior_id: Optional[int] = 0

