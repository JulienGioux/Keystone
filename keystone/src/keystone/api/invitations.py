from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.keystone.models.user import User
from src.keystone.core.db import AsyncSessionLocal

async def get_db():
    # This will be overridden in tests
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user() -> User | None:
    # This is the real dependency that we will override in tests
    return None

router = APIRouter()

# I'll add a dummy endpoint so the router is valid
@router.get("/")
async def get_invitations():
    return []
