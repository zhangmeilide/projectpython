from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from models.shop import Shop
from schemas.clue import ClueCreate,ClueUpdate

class ShopService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_shops(
        self,
        db: Session,
        org_id: int,
        shop_name: str = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[dict]:
        # 构建查询
        query = db.query(Shop)
        if shop_name:
            query = query.filter(Shop.shop_name.like(f"%{shop_name}%"))
            # 获取查询结果
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

        return res








