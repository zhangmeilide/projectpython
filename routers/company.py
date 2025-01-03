from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from db import SessionLocal
from services.user_service import UserService, UserCreate
from services.company_service import CompanyService
from utils.pagination import pagination_params
from typing import Dict,Optional,Union

router = APIRouter()


# 获取数据库 session 的依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
async def create_company(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user)


@router.get("/")
async def get_company(db: Session = Depends(get_db),pagination: Dict[str,int] = Depends(pagination_params)):
    service = CompanyService(db)
    page = pagination["page"]
    page_size = pagination["page_size"]
    return service.get_page_companys(page=page,page_size=page_size)

@router.get("/index")
async def get_company_index(db: Session = Depends(get_db),
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

    service = CompanyService(db)
    return service.get_index_companys(filter_params)

@router.get("/{username}")
async def get_company_by_name(username: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if "message" in user:
        raise HTTPException(status_code=404, detail=user["message"])
    return user
