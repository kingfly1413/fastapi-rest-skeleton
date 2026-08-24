"""Business logic for the Item resource."""

from app.core.exceptions import AppError
from app.models.item import Item
from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, repo: ItemRepository) -> None:
        self.repo = repo

    def create(self, data: ItemCreate, owner_id: int) -> Item:
        item = Item(
            title=data.title,
            description=data.description,
            price=data.price,
            owner_id=owner_id,
        )
        return self.repo.add(item)

    def get(self, item_id: int) -> Item:
        item = self.repo.get(item_id)
        if item is None:
            raise AppError(status_code=404, detail="Item not found")
        return item

    def list_by_owner(
        self, owner_id: int, *, limit: int = 100, offset: int = 0
    ) -> list[Item]:
        return self.repo.list_by_owner(owner_id, limit=limit, offset=offset)

    def update(self, item_id: int, data: ItemUpdate) -> Item:
        item = self.get(item_id)
        if data.title is not None:
            item.title = data.title
        if data.description is not None:
            item.description = data.description
        if data.price is not None:
            item.price = data.price
        return self.repo.add(item)

    def delete(self, item_id: int) -> None:
        item = self.get(item_id)
        self.repo.delete(item)
