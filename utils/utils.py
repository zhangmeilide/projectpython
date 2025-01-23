from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.org import Org

def get_org_info(db: Session, org_id: int) -> dict:
    org_info = db.query(Org).filter(Org.deleted_at.is_(None), Org.id == org_id).first()
    if not org_info:
        raise HTTPException(status_code=404, detail="机构不存在")
    return {
        "province_id": org_info.province_id,
        "city_id": org_info.city_id,
        "county_id": org_info.county_id,
        "street_id": org_info.street_id
    }