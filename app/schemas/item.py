"""Pydantic schemas for the Item resource."""

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    price: float = 0.0


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None


class ItemOut(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
