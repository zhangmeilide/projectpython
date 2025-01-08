from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from services.clue_service import ClueService
from routers.user import get_current_user
from typing import Dict,Optional,Union
from db import get_db
router = APIRouter()
@router.get("/")
def get_clue_list_route(
    clue_name: str = None,
    assign_status: int = 0,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    org_id = current_user["org_id"]  # 假设 current_user 包含 org_id
    dept_id = current_user["dept_id"]  # 假设 current_user 包含 dept_id

    skip = (page - 1) * limit
    service = ClueService()
    clues = service.get_all_clues(
        db=db,
        org_id=org_id,
        dept_id=dept_id,
        clue_name=clue_name,
        assign_status=assign_status,
        skip=skip,
        limit=limit
    )
    return clues

@router.get("/index")
async def get_clue_index(db: Session = Depends(get_db),
                            page: int = Query(1, ge=1, description="当前页码"),
                            page_size: int = Query(10, ge=1, le=100, description="每页数据量"),
                            company_name: Optional[str] = Query(None, description="公司名称用于模糊搜索"),
                            company_address: Optional[str] = Query(None, description="公司地址用于模糊搜索"),
                            industry: Optional[str] = Query(None, description="行业"),
                            ):
    # 正确的方式是先定义字典
    filter_params: Dict[str, Union[int, Optional[str]]] = {
        "page": page,
        "page_size": page_size,
        "company_name": company_name,
        "company_address": company_address,
        "industry": industry,
    }

    service = ClueService(db)
    return service.get_clues(filter_params)
