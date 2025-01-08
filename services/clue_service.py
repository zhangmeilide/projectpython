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
        # 构建查询
        query = db.query(Clue, ClueOrg).join(ClueOrg).filter(
            ClueOrg.org_id == org_id,
            ClueOrg.dept_id == dept_id
        )
        if clue_name:
            query = query.filter(Clue.clue_name.like(f"%{clue_name}%"))
        if assign_status:
            query = query.filter(ClueOrg.assign_status == assign_status)

            # 获取查询结果
        results = query.offset(skip).limit(limit).all()

        # 转换为字典列表
        ASSIGN_STATUS_MAP = {
            1000: "未分派（创建）",
            1001: "上级派发（来我这的）",
            1002: "其他部门移交（来我这的）",
            2001: "分派下级的（给别人的）",
            2002: "移交部门的（给别人的）",
            3001: "下级机构-退回给我的",
            3002: "同机构不同部门-退回给我的",
            4001: "我退回给-上级机构",
            4002: "我退回给-同机构其他部门的",
            5001: "拉回来的",
            5002: "拉走的",
        }

        clues = []
        for clue, clue_org in results:
            clues.append({
                "id": clue.id,
                "clue_name": clue.clue_name,
                "clue_url": clue.clue_url,
                "assign_status": clue_org.assign_status,
                "assign_status_text": ASSIGN_STATUS_MAP.get(clue_org.assign_status, "未知状态"),
                # 如果需要更多字段，可继续添加
                "created_at": clue.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # 格式化时间
                "updated_at": clue.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            })

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
