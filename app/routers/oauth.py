import secrets

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.database import get_session
from app.schemas.auth import TokenResponse
from app.services.oauth import (
    exchange_github_code,
    exchange_google_code,
    get_github_auth_url,
    get_google_auth_url,
    get_or_create_oauth_user,
)
from app.services.token import create_access_token, create_refresh_token

router = APIRouter()


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
    user = get_or_create_oauth_user(session, email, "google", user_info["sub"])
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
    user = get_or_create_oauth_user(session, email, "github", str(user_info["id"]))
    return TokenResponse(
        access_token=create_access_token(user.email),
        refresh_token=create_refresh_token(user.email),
    )
