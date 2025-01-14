from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from services.clue_service import ClueService
from routers.user import get_current_user
from schemas.clue import ClueCreate,ClueUpdate
from typing import Dict
from db import get_db
router = APIRouter()
@router.get("/")
def get_clue_list_route(
    clue_name: str = None,
    assign_status: int = 0,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    org_id = current_user["org_id"]  # 假设 current_user 包含 org_id
    dept_id = current_user["dept_id"]  # 假设 current_user 包含 dept_id

    skip = (page - 1) * limit
    service = ClueService(db)
    clues = service.get_all_clues(
        db=db,
        org_id=org_id,
        dept_id=dept_id,
        clue_name=clue_name,
        assign_status=assign_status,
        skip=skip,
        limit=limit
    )
    return clues

@router.post("/")
async def create_clue_transaction(clue: ClueCreate, db: Session = Depends(get_db)):
    clue_service = ClueService(db)
    return clue_service.create_clue_transaction(clue)

@router.put("/{id}")
async def update_clue(id:int, clue: ClueUpdate, db: Session = Depends(get_db)):
    clue_service = ClueService(db)
    return clue_service.update_clue(id,clue)

@router.delete("/{id}")
async def delete_clue(id:int, db: Session = Depends(get_db)):
    clue_service = ClueService(db)
    return clue_service.delete_clue(id)







