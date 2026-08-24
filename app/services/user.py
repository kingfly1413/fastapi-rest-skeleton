"""Business logic for the User resource."""

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import AppError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def create(self, data: UserCreate) -> User:
        if self.repo.get_by_email(data.email):
            raise AppError(status_code=409, detail="Email already registered")
        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
        )
        try:
            return self.repo.add(user)
        except IntegrityError:
            self.repo.db.rollback()
            raise AppError(status_code=409, detail="Email already registered")

    def get(self, user_id: int) -> User:
        user = self.repo.get(user_id)
        if user is None:
            raise AppError(status_code=404, detail="User not found")
        return user

    def get_by_email(self, email: str) -> User:
        user = self.repo.get_by_email(email)
        if user is None:
            raise AppError(status_code=404, detail="User not found")
        return user

    def list(self, *, limit: int = 100, offset: int = 0) -> list[User]:
        return list(self.repo.list(limit=limit, offset=offset))

    def update(self, user_id: int, data: UserUpdate) -> User:
        user = self.get(user_id)
        if data.email is not None:
            user.email = data.email
        if data.full_name is not None:
            user.full_name = data.full_name
        if data.password is not None:
            user.hashed_password = hash_password(data.password)
        if data.is_active is not None:
            user.is_active = data.is_active
        return self.repo.add(user)

    def delete(self, user_id: int) -> None:
        user = self.get(user_id)
        self.repo.delete(user)
