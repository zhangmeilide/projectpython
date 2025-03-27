from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShopCreate(BaseModel):
    # 已有的 ShopCreate 类保持不变
    shop_name: str
    shop_url: str
    company_name: str
    company_id: int
    # 其他字段...

class ShopUpdate(BaseModel):
    """
    用于更新店铺信息的 Schema
    """
    shop_name: Optional[str] = None
    shop_url: Optional[str] = None
    shop_logo: Optional[str] = None
    link_man: Optional[str] = None
    link_phone: Optional[str] = None
    shop_type_id: Optional[int] = None
    shop_type_name: Optional[str] = None
    shop_cate: Optional[str] = None
    shop_address: Optional[str] = None


