from fastapi import HTTPException
from models.org import Org
from sqlalchemy.orm import Session

class OrgService:
    def __init__(self, db: Session):
        self.db = db  # 接受 db 会话

    def get_org_info(self, org_id) -> dict:
        org_info = self.db.query(Org).filter(Org.deleted_at.is_(None), Org.id == org_id).first()
        if not org_info:
            raise HTTPException(status_code=404, detail="机构不存在")
        return {
            "province_id": org_info.province_id,
            "city_id": org_info.city_id,
            "county_id": org_info.county_id,
            "street_id": org_info.street_id
        }