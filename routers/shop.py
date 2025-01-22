from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from services.shop_service import ShopService
from routers.user import get_current_user
from schemas.shop import ShopCreate
from typing import Dict
from db import get_db
router = APIRouter()
@router.get("/")
def get_shop_list_route(
    shop_name: str = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    org_id = current_user["org_id"]  # ¼ÙÉè current_user °üº¬ org_id
    skip = (page - 1) * limit
    service = ShopService(db)
    result = service.get_all_shops(
        db=db,
        org_id=org_id,
        shop_name=shop_name,
        skip=skip,
        limit=limit
    )
    return result


@router.post("/")
async def create_shop(
        shop: ShopCreate,
        db: Session = Depends(get_db),
        current_user: Dict = Depends(get_current_user)
):
    service = ShopService(db)
    return service.create_shop(shop,current_user)



