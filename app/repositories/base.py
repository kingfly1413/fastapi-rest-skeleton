"""Generic base repository to remove CRUD boilerplate."""

from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Minimal read/write helpers shared by concrete repositories."""

    model: type[ModelType]

    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, obj_id: int) -> ModelType | None:
        return self.db.get(self.model, obj_id)

    def list(self, *, limit: int = 100, offset: int = 0) -> Sequence[ModelType]:
        stmt = select(self.model).offset(offset).limit(limit)
        return self.db.scalars(stmt).all()

    def add(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.commit()
