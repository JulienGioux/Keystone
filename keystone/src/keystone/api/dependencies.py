from typing import AsyncGenerator
from uuid import UUID

from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.keystone.core.db import AsyncSessionLocal
from src.keystone.models.user import User


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    x_test_user_id: str | None = Header(None, alias="X-Test-User-Id"),
) -> User:
    if not x_test_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = await db.get(User, UUID(x_test_user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
