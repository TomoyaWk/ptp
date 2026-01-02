from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.user import User
from app.schemas.user import UserResponse
from app.api.endpoints.auth import get_current_user


router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def get_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    ユーザー一覧を取得する
    """
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users




