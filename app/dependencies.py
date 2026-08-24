"""Dependency-injection wiring: repositories and current user."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.exceptions import AppError
from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User
from app.repositories.item import ItemRepository
from app.repositories.user import UserRepository

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user_repository(db: Annotated[Session, Depends(get_db)]) -> UserRepository:
    return UserRepository(db)


def get_item_repository(db: Annotated[Session, Depends(get_db)]) -> ItemRepository:
    return ItemRepository(db)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    """Decode the JWT and return the authenticated user, or raise 401."""
    subject = decode_access_token(token)
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = repo.get_by_email(subject)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_active_user(user: Annotated[User, Depends(get_current_user)]) -> User:
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user


def get_current_superuser(user: Annotated[User, Depends(get_current_active_user)]) -> User:
    # Placeholder hook for role-based authorization.
    return user
