"""
Example router — shows how to add new protected endpoints.
Copy this file and wire a new router in app/main.py.
"""
from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, require_role
from app.models.user import Role, User

router = APIRouter()


@router.get("/public")
def public_endpoint():
    return {"message": "Anyone can access this"}


@router.get("/protected")
def protected_endpoint(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.email}"}


@router.get("/admin-only")
def admin_endpoint(_: User = Depends(require_role(Role.ADMIN))):
    return {"message": "Admin access granted"}
