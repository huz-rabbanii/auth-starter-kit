import secrets

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.services.oauth import (
    exchange_github_code,
    exchange_google_code,
    get_github_auth_url,
    get_google_auth_url,
)
from app.services.token import create_access_token, create_refresh_token

router = APIRouter()


def _get_or_create_oauth_user(session: Session, email: str, provider: str, oauth_id: str) -> User:
    user = session.exec(select(User).where(User.email == email)).first()
    if user:
        return user
    user = User(email=email, oauth_provider=provider, oauth_id=oauth_id)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/google")
def google_login():
    state = secrets.token_urlsafe(32)
    return RedirectResponse(get_google_auth_url(state))


@router.get("/google/callback")
async def google_callback(code: str, session: Session = Depends(get_session)):
    try:
        user_info = await exchange_google_code(code)
    except Exception:
        raise HTTPException(status_code=400, detail="Google OAuth failed")
    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Could not retrieve email from Google")
    user = _get_or_create_oauth_user(session, email, "google", user_info["sub"])
    return TokenResponse(
        access_token=create_access_token(user.email),
        refresh_token=create_refresh_token(user.email),
    )


@router.get("/github")
def github_login():
    state = secrets.token_urlsafe(32)
    return RedirectResponse(get_github_auth_url(state))


@router.get("/github/callback")
async def github_callback(code: str, session: Session = Depends(get_session)):
    try:
        user_info = await exchange_github_code(code)
    except Exception:
        raise HTTPException(status_code=400, detail="GitHub OAuth failed")
    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Could not retrieve email from GitHub")
    user = _get_or_create_oauth_user(session, email, "github", str(user_info["id"]))
    return TokenResponse(
        access_token=create_access_token(user.email),
        refresh_token=create_refresh_token(user.email),
    )
