"""User resource router."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_user_repository
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    return UserService(repo).create(data)


@router.get("", response_model=list[UserOut])
def list_users(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    limit: int = 100,
    offset: int = 0,
) -> list[User]:
    return UserService(repo).list(limit=limit, offset=offset)


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    return UserService(repo).get(user_id)


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    data: UserUpdate,
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    return UserService(repo).update(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> None:
    UserService(repo).delete(user_id)
