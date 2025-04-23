import datetime
from sqlalchemy.orm import Session
from models.website import Website
from schemas.website import WebsiteCreate, WebsiteUpdate
class WebsiteService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_websites(self, website_name: str = "", page: int = 0, size: int = 10):
        query = self.db.query(Website).filter(Website.deleted_at.is_(None))
        if website_name:
            query = query.filter(Website.website_name.like(f"%{website_name}%"))
        total = query.count()
        results = query.offset(page * size).limit(size).all()
        res = []
        for item in results:
            res.append({
                "id": item.id,
                "website_name": item.website_name,
                "website_url": item.website_url,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return {
            'total': total,
            'page': page,
            'size': size,
            'data': res
        }

    def create_website(self, website: WebsiteCreate, current_user: dict):
        province_id = current_user["province_id"]
        city_id = current_user["city_id"]
        county_id = current_user["county_id"]
        # 修正：使用datetime模块中的datetime类来获取当前时间
        now = datetime.datetime.now()
        db_website = Website(
            **website.model_dump(),  
            province_id=province_id, 
            city_id=city_id, 
            county_id=county_id,
            created_at=now,
            updated_at=now
        )
        self.db.add(db_website)
        self.db.commit()
        self.db.refresh(db_website)
        response_data = {
            "id": db_website.id,
            "website_name": db_website.website_name,
            "website_url": db_website.website_url,
            # 修改时间格式
            "created_at": db_website.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": db_website.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "province_id": db_website.province_id,
            "city_id": db_website.city_id,
            "county_id": db_website.county_id,
        }
        return response_data