"""Item resource router (protected by JWT)."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_active_user, get_item_repository
from app.models.item import Item
from app.models.user import User
from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemOut, ItemUpdate
from app.services.item import ItemService

router = APIRouter(prefix="/items", tags=["items"])

# NOTE: items are queried by owner_id passed from the authenticated user.
# The router does not yet enforce that `item.owner_id == current_user.id` on
# get/update/delete -- add that ownership check in the service for production.


@router.post("", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(
    data: ItemCreate,
    repo: Annotated[ItemRepository, Depends(get_item_repository)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Item:
    return ItemService(repo).create(data, owner_id=current_user.id)


@router.get("", response_model=list[ItemOut])
def list_items(
    repo: Annotated[ItemRepository, Depends(get_item_repository)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    limit: int = 100,
    offset: int = 0,
) -> list[Item]:
    return ItemService(repo).list_by_owner(current_user.id, limit=limit, offset=offset)


@router.get("/{item_id}", response_model=ItemOut)
def get_item(
    item_id: int,
    repo: Annotated[ItemRepository, Depends(get_item_repository)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Item:
    return ItemService(repo).get(item_id)


@router.patch("/{item_id}", response_model=ItemOut)
def update_item(
    item_id: int,
    data: ItemUpdate,
    repo: Annotated[ItemRepository, Depends(get_item_repository)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Item:
    return ItemService(repo).update(item_id, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    repo: Annotated[ItemRepository, Depends(get_item_repository)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> None:
    ItemService(repo).delete(item_id)
