from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.dept import Dept
from services.dept_service import DeptService
from routers.user import get_current_user
from schemas.dept import DeptCreate, DeptUpdate
from typing import Dict
from db import get_db

router = APIRouter()

@router.get("/")
def get_dept_list_route(
    dept_name: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    org_id = current_user["org_id"]
    print(org_id)

    skip = (page - 1) * limit
    service = DeptService(db)
    result = service.get_all_depts(
        org_id=org_id,
        dept_name=dept_name,
        page=skip,
        limit=limit
    )
    return result

@router.post("/")
async def create_dept(
    dept: DeptCreate,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    service = DeptService(db)
    return service.create_dept(dept, current_user)

@router.put("/{dept_id}")
async def update_dept(
    dept_id: int,
    dept: DeptUpdate,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    service = DeptService(db)
    updated_dept = service.update_dept(dept_id, dept, current_user)
    if not updated_dept:
        raise HTTPException(status_code=404, detail="Dept not found")
    return updated_dept

@router.delete("/{dept_id}")
async def delete_dept(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    service = DeptService(db)
    deleted = service.delete_dept(dept_id, current_user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Dept not found")
    return {"message": "部门删除成功"}