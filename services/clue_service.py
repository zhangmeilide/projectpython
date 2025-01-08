from typing import List, Optional, Dict,Union
from sqlalchemy.orm import Session
from models.company import Company
from models.clue import Clue,ClueOrg
from schemas.clue import ClueOut

class ClueService:
    def get_all_clues(
        self,
        db: Session,
        org_id: int,
        dept_id: int,
        clue_name: str = None,
        assign_status: int = 0,
        skip: int = 0,
        limit: int = 10
    ) -> List[dict]:
        query = db.query(Clue).join(ClueOrg).filter(
   ClueOrg.org_id == org_id,
            ClueOrg.dept_id == dept_id
        )
        if clue_name:
            query = query.filter(Clue.clue_name.like(f"%{clue_name}%"))
        if assign_status:
            query = query.filter(ClueOrg.assign_status == assign_status)

        clues = query.offset(skip).limit(limit).all()
        return clues

    def get_clues(self, filter_params:Dict[str, Union[int,Optional[str]]] ) -> dict:
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
