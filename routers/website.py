from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from schemas.website import WebsiteCreate, WebsiteUpdate
from services.website_service import WebsiteService
from typing import List, Dict
from routers.user import get_current_user

router = APIRouter()

@router.get("/")
def get_all_websites(
    website_name: str = "",
    page: int = 0,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    service = WebsiteService(db)
    return service.get_all_websites(website_name, page, size)

@router.post("/")
def create_website(
    website: WebsiteCreate,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    service = WebsiteService(db)
    new_website = service.create_website(website, current_user)
    return {
        "msg": "新增成功",
        "status": 200,
        "data": new_website
    }
