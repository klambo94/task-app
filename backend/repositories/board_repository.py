from sqlalchemy.orm import Session

from models.board_model import Board


def get_boards_by_user(session: Session, user_id: int) -> list[type[Board]]:
    return session.query(Board).filter(Board.user_id == user_id).all()

def create_board(session: Session, name: str, description: str, user_id: str) -> Board:
    board = Board(name=name, description=description, user_id=user_id)
    session.add(board)
    session.commit()
    session.refresh(board)
    return board

def delete_board(session: Session, board_id: int) -> None:
    board = session.query(Board).filter(Board.id == board_id).first()
    session.delete(board)
    session.commit()