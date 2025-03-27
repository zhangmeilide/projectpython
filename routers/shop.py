from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models import org
from services.org_service import OrgService
from services.shop_service import ShopService
from routers.user import get_current_user
from schemas.shop import ShopCreate, ShopUpdate  # 假设存在 ShopUpdate 这个 schema
from typing import Dict
from db import get_db
import logging
from fastapi.responses import FileResponse
import pandas as pd
import os

# 配置日志记录
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

router = APIRouter()

@router.get("/")
def get_shop_list_route(
    shop_name: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    org_id = current_user["org_id"]
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
    return service.create_shop(shop, current_user)

@router.put("/{shop_id}")
async def update_shop(
    shop_id: int,
    shop: ShopUpdate,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    service = ShopService(db)
    updated_shop = service.update_shop(shop_id, shop, current_user)
    if not updated_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return updated_shop

@router.delete("/{shop_id}")
async def delete_shop(
    shop_id: int,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    service = ShopService(db)
    deleted = service.delete_shop(shop_id, current_user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Shop not found")
    return {"message": "Shop deleted successfully"}

@router.get("/export/excel")
def export_shops_to_excel(
    platform_name: str = "",
    shop_name: str = "",
    link_man: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    org_id = current_user["org_id"]
    skip = (page - 1) * limit
    service = ShopService(db)
    shops = service.get_export_shops(
        db=db,
        org_id=org_id,
        platform_name=platform_name,
        shop_name=shop_name,
        link_man=link_man,
        skip=skip,
        limit=limit
    )

    # 将查询结果转换为DataFrame
    df = pd.DataFrame([{
        "平台名称": shop.platform_name,
        "网店名称": shop.shop_name,
        "店铺链接": shop.shop_url,
        "店铺logo图片地址": shop.shop_logo,
        "店铺联系人名称": shop.link_man
    } for shop in shops])

    # 导出DataFrame到Excel文件
    file_dir = "static/reports"
    # 确保目录存在
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, "shops_export.xlsx")
    df.to_excel(file_path, index=False)
    # 返回文件响应
    # response = FileResponse(file_path, filename="shops_export.xlsx")这种输出是文件流吗
    # 返回文件路径
    return {"xlsx_path": file_path}




