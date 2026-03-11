from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.board_schema import BoardResponse
from repositories import board_repository

router = APIRouter(prefix="/api/boards", tags=["boards"])

@router.get("/", response_model=list[BoardResponse])
def get_boards(session: Session = Depends(get_db)):
    return board_repository.get_boards_by_user(session)