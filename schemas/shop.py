from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShopCreate(BaseModel):
    shop_name: str
    shop_url: str
    company_id: int
    company_name: str


