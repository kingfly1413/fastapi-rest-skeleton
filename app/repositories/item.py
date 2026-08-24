"""Data-access layer for Item."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.item import Item
from app.repositories.base import BaseRepository


class ItemRepository(BaseRepository[Item]):
    model = Item

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def list_by_owner(
        self, owner_id: int, *, limit: int = 100, offset: int = 0
    ) -> list[Item]:
        stmt = (
            select(Item).where(Item.owner_id == owner_id).offset(offset).limit(limit)
        )
        return list(self.db.scalars(stmt).all())
