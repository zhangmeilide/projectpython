# app/schemas/clue.py
from pydantic import BaseModel
from datetime import datetime

class ClueOut(BaseModel):
    id: int
    clue_name: str
    clue_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
