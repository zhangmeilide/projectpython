from sqlalchemy.orm import Session
from models.dept import Dept
from schemas.dept import DeptCreate, DeptUpdate

class DeptService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_depts(self, org_id: int, dept_name: str = "", page: int = 0, limit: int = 10):
        query = self.db.query(Dept).filter(Dept.org_id == org_id)
        if dept_name:
            query = query.filter(Dept.dept_name.like(f"%{dept_name}%"))
        return query.offset(page * limit).limit(limit).all()

    def create_dept(self, dept: DeptCreate, current_user):
        org_id = current_user["org_id"]
        # 排除 dept.dict() 中的 org_id 字段
        new_dept = Dept(**dept.model_dump(exclude={"org_id"}), org_id=org_id)
        self.db.add(new_dept)
        self.db.commit()
        self.db.refresh(new_dept)
        return new_dept

    def update_dept(self, dept_id: int, dept: DeptUpdate, current_user):
        org_id = current_user["org_id"]
        db_dept = self.db.query(Dept).filter(Dept.id == dept_id, Dept.org_id == org_id).first()
        if db_dept:
            for key, value in dept.model_dump(exclude_unset=True).items():
                setattr(db_dept, key, value)
            self.db.commit()
            self.db.refresh(db_dept)
            return db_dept
        return None

    def delete_dept(self, dept_id: int, current_user):
        org_id = current_user["org_id"]
        db_dept = self.db.query(Dept).filter(Dept.id == dept_id, Dept.org_id == org_id).first()
        if db_dept:
            self.db.delete(db_dept)
            self.db.commit()
            return True
        return False