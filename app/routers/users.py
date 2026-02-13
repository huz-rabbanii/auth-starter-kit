from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies import get_current_user, require_role
from app.models.user import Role, User
from app.schemas.auth import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserResponse])
def list_users(
    session: Session = Depends(get_session),
    _: User = Depends(require_role(Role.ADMIN)),
):
    return session.exec(select(User)).all()
