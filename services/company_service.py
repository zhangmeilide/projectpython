from typing import List, Optional, Dict,Union

from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.company import Company
from models.user import User


class UserCreate(BaseModel):
    name: str
    mobile: str
    org_id: Optional[int] = 0

class CompanyService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> dict:
        print(f"{user}")
        db_user = User(name=user.name, mobile=user.mobile,org_id=user.org_id)
        print(f"{db_user}")
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return {"message": "用户创建成功", "user": db_user}

    def get_all_companys(self) -> List[dict]:
        companys = self.db.query(Company).all()
        return [{"id": company.id, "company_name": company.company_name, "company_address": company.company_address} for company in companys]

    def get_page_companys(self, page: int = 1, page_size: int = 10) -> dict:
        query = self.db.query(Company)
        total_items = query.count()  # 获取总数
        total_pages = (total_items + page_size - 1) // page_size  # 计算总页数

        companies = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            "data": [
                {"id": company.id, "company_name": company.company_name, "company_address": company.company_address} for
                company in companies],
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages
            }
        }

    def get_index_companys(self, filter_params:Dict[str, Union[int,Optional[str]]] ) -> dict:
        print(filter_params)
        # 解包字典中的分页参数
        page = filter_params.get("page", 1)
        page_size = filter_params.get("page_size", 10)
        # 构建查询
        query = self.db.query(Company)

        # 根据查询条件动态添加过滤
        if filter_params.get("company_name"):
            query = query.filter(Company.company_name.like(f"%{filter_params['company_name']}%"))
        if filter_params.get("company_address"):
            query = query.filter(Company.company_address.like(f"%{filter_params['company_address']}%"))
        if filter_params.get("industry"):
            query = query.filter(Company.industry == filter_params["industry"])

        # 计算总数和分页
        total_items = query.count()
        total_pages = (total_items + page_size - 1) // page_size

        # print(f"Executing query: {query}")
        # 执行分页查询
        companies = query.offset((page - 1) * page_size).limit(page_size).all() or []
        # print(f"Found companies: {companies}")  # 查看返回的结果
        return {
            "data": [
                self._format_company(company) for
                company in companies],
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages
            }
        }

    def _format_company(self, company: Company) -> dict:
        return  {
            "id": company.id,
            "company_name": company.company_name,
            "company_address": company.company_address,
            "industry": company.industry,
        }

    def get_user_by_username(self, name: str) -> dict:
        # print(f"{name}")
        user = self.db.query(User).filter(User.name == name).first()
        if user:
            return {"id": user.id, "mobile": user.mobile, "name": user.name}
        return {"message": f"用户 {name} 不存在"}