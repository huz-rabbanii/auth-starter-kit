from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Role(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: Optional[str] = None  # None for OAuth-only users
    role: Role = Field(default=Role.USER)
    is_active: bool = Field(default=True)
    oauth_provider: Optional[str] = None  # "google" | "github"
    oauth_id: Optional[str] = None
