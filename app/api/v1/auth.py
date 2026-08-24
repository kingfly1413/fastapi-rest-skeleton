"""Authentication: OAuth2 password login and current-user info."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.security import create_access_token, verify_password
from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserOut

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    repo = UserRepository(db)
    user = repo.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=user.email)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def read_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    return current_user
