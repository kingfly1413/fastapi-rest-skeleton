"""Data-access layer for User."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.scalars(stmt).one_or_none()
