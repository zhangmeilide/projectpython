from fastapi import HTTPException,Depends
from typing import List
from sqlalchemy import Null
from sqlalchemy.orm import Session
from services.org_service import OrgService
from models.org import Org
from models.shop import Shop
from schemas.clue import ClueCreate,ClueUpdate
from schemas.shop import ShopCreate
from datetime import datetime
from utils.utils import get_org_info
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.shop import Shop
from schemas.shop import ShopCreate, ShopUpdate
from typing import Dict

class ShopService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_shops(self, db: Session, org_id: int, shop_name: str | None = None, skip: int = 0, limit: int = 10):
        # 构建查询
        query = db.query(Shop).filter(Shop.deleted_at.is_(None))  # 过滤掉已删除的数据
        if shop_name:
            query = query.filter(Shop.shop_name.like(f"%{shop_name}%"))
            # 获取查询结果
            # 获取总条数
        total = query.count()
        results = query.offset(skip).limit(limit).all()

        res = []
        for item in results:
            res.append({
                "id": item.id,
                "shop_name": item.shop_name,
                "shop_url": item.shop_url,
                # 如果需要更多字段，可继续添加
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # 格式化时间
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            })

        return {
            'total': total,
            'data': res
        }

    def get_export_shops(self, db: Session, org_id: int, platform_name: str = "", shop_name: str = "", link_man: str = "", skip: int = 0, limit: int = 10):
        query = db.query(Shop)
        org_info = get_org_info(self.db,org_id)  # Use injected OrgService
        if org_info['province_id']:
            query = query.filter(Shop.province_id == org_info['province_id'])
        if org_info['city_id']:
            query = query.filter(Shop.city_id == org_info['city_id'])
        if org_info['county_id']:
            query = query.filter(Shop.county_id == org_info['county_id'])
        if platform_name:
            query = query.filter(Shop.platform_name.contains(platform_name))
        if shop_name:
            query = query.filter(Shop.shop_name.contains(shop_name))
        if link_man:
            query = query.filter(Shop.link_man.contains(link_man))
        return query.offset(skip).limit(limit).all()

    def create_shop(self,shop: ShopCreate,current_user:dict) -> dict:
        org_id = current_user['org_id']
        org_info = get_org_info(self.db,org_id)  # Use injected OrgService
        db_data = Shop(
            shop_name=shop.shop_name,
            shop_url=shop.shop_url,
            company_name=shop.company_name,
            company_id=shop.company_id,
            province_id=org_info['province_id'],
            city_id=org_info['city_id'],
            county_id=org_info['county_id'],
            street_id=org_info['street_id'],
        )
        self.db.add(db_data)
        self.db.commit()
        self.db.refresh(db_data)
        return {"status":200,"message": "店铺创建成功","data":db_data}

    def get_org_info(self,org_id)->dict:
        org_info = self.db.query(Org).filter(Org.deleted_at.is_(None),Org.id == org_id).first()
        if not org_info:
            raise HTTPException(status_code=404, detail="机构不存在")
        return {
            "province_id": org_info.province_id,
            "city_id": org_info.city_id,
            "county_id": org_info.county_id,
            "street_id": org_info.street_id
        }

    def delete_shop_bak(self, shop_id: int) -> dict:
        # 查询要删除的店铺
        shop = self.db.query(Shop).filter(Shop.id == shop_id, Shop.deleted_at.is_(None)).first()
        if not shop:
            return {"status": 404, "message": "店铺不存在或已被删除"}

        # 设置 deleted_at 为当前时间
        # Bug修复: 为类“Shop”的属性“deleted_at”赋值时，需要赋值为datetime类型的值
        # Bug修复: 使用datetime.now()代替func.now()来为deleted_at赋值
        shop.deleted_at = datetime.now() # type: ignore
        self.db.commit()
        self.db.refresh(shop)

        return {"status": 200, "message": "店铺删除成功", "shop": shop}

    def restore_shop(self, shop_id: int) -> dict:
        # 查询被软删除的店铺
        shop = self.db.query(Shop).filter(Shop.id == shop_id, Shop.deleted_at.is_not(None)).first()
        if not shop:
            return {"status": 404, "message": "店铺不存在或未被删除"}

        # 恢复数据
        # Bug修复: 将 shop.deleted_at 的值设置为 None，而不是 Null
        shop.deleted_at = None  # type: ignore
        self.db.commit()
        self.db.refresh(shop)

        return {"status": 200, "message": "店铺恢复成功", "shop": shop}

    def update_shop(self, shop_id: int, shop: ShopUpdate, current_user: Dict):
        db_shop = self.db.query(Shop).filter(Shop.id == shop_id).first()
        if not db_shop:
            return None
        for var, value in vars(shop).items():
            if value is not None:
                setattr(db_shop, var, value)
        self.db.commit()
        self.db.refresh(db_shop)
        return db_shop

    def delete_shop(self, shop_id: int, current_user: Dict):
        db_shop = self.db.query(Shop).filter(Shop.id == shop_id).first()
        if not db_shop:
            return False
       # self.db.delete(db_shop)
       # self.db.commit()
        db_shop.deleted_at = None  # type: ignore
        self.db.commit()
        self.db.refresh(db_shop)
        return True




