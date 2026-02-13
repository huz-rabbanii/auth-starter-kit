# auth-starter-kit

Production-ready authentication backend you can clone and use in any project — so you never write auth from scratch again.

Built with **FastAPI + SQLite + JWT + OAuth**.

---

## The Problem

Every app needs auth. Every time you start a new project you spend days on login, tokens, OAuth, and role permissions before touching your actual idea.

This repo solves that. Clone it, fill in your keys, and auth is done in 10 minutes.

---

## What's Included

| Feature | Details |
|---|---|
| Email/password auth | Register, login, bcrypt password hashing |
| JWT tokens | Short-lived access token + refresh token |
| Google OAuth | Login with Google in 2 steps |
| GitHub OAuth | Login with GitHub in 2 steps |
| Role-based access | `user`, `moderator`, `admin` roles built in |
| Rate limiting | Brute-force protection on login/register |

---

## Quick Start

```bash
git clone https://github.com/huz-rabbanii/auth-starter-kit
cd auth-starter-kit

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt

cp .env.example .env           # then fill in your keys
uvicorn app.main:app --reload
```

Open **http://localhost:8000/docs** to see and test all endpoints interactively.

---

## Environment Variables

```env
SECRET_KEY=your-long-random-string
REFRESH_SECRET_KEY=another-long-random-string

# Optional — leave blank to disable
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

FRONTEND_URL=http://localhost:3000
```

Generate secret keys:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## API Endpoints

```
POST   /auth/register          Create a new account
POST   /auth/login             Login and get tokens
POST   /auth/refresh           Get a new access token
GET    /auth/me                Get current user info

GET    /auth/google            Redirect to Google login
GET    /auth/google/callback   Google OAuth callback

GET    /auth/github            Redirect to GitHub login
GET    /auth/github/callback   GitHub OAuth callback

GET    /users/                 List all users (admin only)
GET    /health                 Health check
```

---

## Using It In Your Own Project

**1. Register a user**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret123"}'
```

**2. Login and get a token**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret123"}'
```

**3. Access a protected route**
```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**4. Protect your own routes**
```python
from app.dependencies import get_current_user, require_role
from app.models.user import Role

# Any logged-in user
@router.get("/dashboard")
def dashboard(user = Depends(get_current_user)):
    return {"hello": user.email}

# Admins only
@router.get("/admin")
def admin_panel(user = Depends(require_role(Role.ADMIN))):
    return {"message": "Welcome admin"}
```

---

## Project Structure

```
app/
├── main.py          # App entry point
├── config.py        # Settings from .env
├── database.py      # SQLite setup
├── dependencies.py  # Auth guards (get_current_user, require_role)
├── models/          # Database models
├── schemas/         # Request/response shapes
├── routers/         # auth, oauth, users routes
├── services/        # JWT token logic, OAuth exchange
└── middleware/      # Rate limiting
```

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — API framework
- [SQLModel](https://sqlmodel.tiangolo.com/) — Database ORM
- [python-jose](https://github.com/mpdavis/python-jose) — JWT tokens
- [passlib](https://passlib.readthedocs.io/) — Password hashing
- [slowapi](https://github.com/laurentS/slowapi) — Rate limiting
- [httpx](https://www.python-httpx.org/) — OAuth HTTP calls
