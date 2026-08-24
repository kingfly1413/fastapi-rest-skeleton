"""Aggregate all v1 routers under a single APIRouter."""

from fastapi import APIRouter

from app.api.v1 import auth, items, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(items.router)
