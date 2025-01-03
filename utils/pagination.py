from fastapi import Query,Body
from pydantic import BaseModel
from typing import Dict
class PaginationParams(BaseModel):
    page: int = 1  # 默认页码
    page_size: int = 10  # 默认每页数据量

def pagination_params(pagination: PaginationParams = Body(...)) -> Dict[str, int]:
    return {"page": pagination.page, "page_size": pagination.page_size}