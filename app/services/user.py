from typing import Optional

from sqlmodel import Session, select

from app.models.user import User


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()


def list_all_users(session: Session) -> list[User]:
    return list(session.exec(select(User)).all())
