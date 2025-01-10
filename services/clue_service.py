from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from models.clue import Clue,ClueOrg
from schemas.clue import ClueCreate,ClueUpdate

class ClueService:
    def __init__(self, db: Session):
        self.db = db

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

    # 非事务创建线索
    def create_clue(self, add_data: ClueCreate) -> dict:
        print(f"{add_data}")
        db_data = Clue(
            clue_name=add_data.clue_name,
            clue_url=add_data.clue_url,
            company_id=add_data.company_id,
            company_name=add_data.company_name,
            org_id=add_data.org_id,
            dept_id=add_data.dept_id,
            work_source_flag=add_data.work_source_flag,
            clue_behavior_id=add_data.clue_behavior_id,
        )
        self.db.add(db_data)
        self.db.commit()
        self.db.refresh(db_data)

        # 2. 同时插入 tb_clue_org 数据
        db_clue_org = ClueOrg(
            clue_id=db_data.id,  # 外键关联
            org_id=add_data.org_id,
            dept_id=add_data.dept_id,
            assign_status=1000
        )
        self.db.add(db_clue_org)
        self.db.commit()

        return {"message": "线索和组织创建成功", "clue": db_data, "clue_org": db_clue_org}

    # 创建线索-应用事务
    def create_clue_transaction(self, add_data: ClueCreate) -> dict:
        try:
            # 开始事务
            with self.db.begin():
                db_data = Clue(
                    clue_name=add_data.clue_name,
                    clue_url=add_data.clue_url,
                    company_id=add_data.company_id,
                    company_name=add_data.company_name,
                    org_id=add_data.org_id,
                    dept_id=add_data.dept_id,
                    work_source_flag=add_data.work_source_flag,
                    clue_behavior_id=add_data.clue_behavior_id,
                )
                self.db.add(db_data)
                self.db.flush()
                # 刷新 db_clue_org 获取插入后的数据
                self.db.refresh(db_data)
                # 2. 同时插入 tb_clue_org 数据
                db_clue_org = ClueOrg(
                    clue_id=db_data.id,  # 外键关联
                    org_id=add_data.org_id,
                    dept_id=add_data.dept_id,
                    assign_status=1000
                )
                self.db.add(db_clue_org)
                self.db.flush()
                self.db.refresh(db_clue_org)

                self.db.commit()
        except Exception as e:
            self.db.rollback()  # 发生错误时回滚事务
            raise Exception(f"创建线索：{e}")

        """return {
            "message": "线索和组织创建成功",
            "clue": self._convert_to_dict(db_data),
            "clue_org": self._convert_to_dict(db_clue_org)
        }"""
        # 返回仅包含需要的字段 上面是返回所有的字段
        return {
            "message": "线索和组织创建成功",
            "clue": {
                "id": db_data.id,
                "clue_name": db_data.clue_name,
                "clue_url": db_data.clue_url
            },
            "clue_org": {
                "id": db_clue_org.id,
                "assign_status": db_clue_org.assign_status
            }
        }

    def update_clue(self, id:int,update_data: ClueUpdate) -> dict:
        print(f"{update_data}")
        clue = self.db.query(Clue).filter_by(id=id).first()
        # 如果没有找到线索，抛出 404 错误
        if not clue:
            raise HTTPException(status_code=404, detail="Clue not found")
        try:
            update_dict = {}
            if update_data.clue_name:
                update_dict['clue_name'] = update_data.clue_name.strip()  # 去除空格
            if update_data.clue_url:
                update_dict['clue_url'] = update_data.clue_url
            if update_data.company_id:
                update_dict['company_id'] = update_data.company_id
            if update_data.company_name is not None:
                update_dict['company_name'] = update_data.company_name
            if update_data.org_id:
                update_dict['org_id'] = update_data.org_id
            if update_data.dept_id:
                update_dict['dept_id'] = update_data.dept_id
            if update_data.work_source_flag:
                update_dict['work_source_flag'] = update_data.work_source_flag
            if update_data.clue_behavior_id is not None:
                update_dict['clue_behavior_id'] = update_data.clue_behavior_id

            # 在这里遍历字段并更新
            for field, value in update_dict.items():
                setattr(clue, field, value)  # 动态设置字段的值

            self.db.commit()
            return {
                "status": 200,
                "message": "线索更新成功",
                "clue": {
                    "id": clue.id,
                    "clue_name": clue.clue_name,
                    "clue_url": clue.clue_url,
                    "company_id": clue.company_id,
                    "company_name": clue.company_name,
                    "org_id": clue.org_id,
                    "dept_id": clue.dept_id
                }
            }

        except Exception as e:
            # 发生异常时回滚事务
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"更新线索失败: {e}")

    def delete_clue(self,id)->dict:
        clue = self.db.query(Clue).filter_by(id=id).first()
        if not clue:
            raise HTTPException(status_code=404, detail="线索数据不存在")
        try:
            self.db.delete(clue)
            self.db.commit()
            return {
                "status": 200,
                "message":"线索数据删除成功",
                "id": clue.id
            }

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500,detail=f"删除线索失败:{e}")


    def _convert_to_dict(self, obj):
        """辅助函数，用于将 SQLAlchemy 对象转换为字典"""
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}











