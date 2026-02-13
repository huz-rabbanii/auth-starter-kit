import httpx

from app.config import settings

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USERINFO_URL = "https://api.github.com/user"
GITHUB_EMAIL_URL = "https://api.github.com/user/emails"


def get_google_auth_url(state: str) -> str:
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": f"{settings.FRONTEND_URL}/auth/google/callback",
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{GOOGLE_AUTH_URL}?{query}"


async def exchange_google_code(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        token_res = await client.post(GOOGLE_TOKEN_URL, data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": f"{settings.FRONTEND_URL}/auth/google/callback",
            "grant_type": "authorization_code",
        })
        token_res.raise_for_status()
        access_token = token_res.json()["access_token"]

        user_res = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_res.raise_for_status()
        return user_res.json()


def get_github_auth_url(state: str) -> str:
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "scope": "read:user user:email",
        "state": state,
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{GITHUB_AUTH_URL}?{query}"


async def exchange_github_code(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        token_res.raise_for_status()
        access_token = token_res.json()["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
        user_res = await client.get(GITHUB_USERINFO_URL, headers=headers)
        user_res.raise_for_status()
        user_data = user_res.json()

        if not user_data.get("email"):
            email_res = await client.get(GITHUB_EMAIL_URL, headers=headers)
            email_res.raise_for_status()
            emails = email_res.json()
            primary = next(
                (e["email"] for e in emails if e.get("primary") and e.get("verified")),
                None,
            )
            user_data["email"] = primary

        return user_data
