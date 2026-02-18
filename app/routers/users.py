from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, require_role
from app.models.user import Role, User
from app.schemas.auth import UserResponse
from app.services.user import list_all_users
from app.database import get_session
from sqlmodel import Session

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserResponse])
def list_users(
    session: Session = Depends(get_session),
    _: User = Depends(require_role(Role.ADMIN)),
):
    return list_all_users(session)
