from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.keystone.core.db import AsyncSessionLocal
from src.keystone.crud import invitations as crud
from src.keystone.models.user import User
from src.keystone.schemas.invitation import InvitationCreate, InvitationRead


async def get_db() -> AsyncSession:
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


router = APIRouter()


@router.post("/", response_model=InvitationRead, status_code=201)
async def create_invitation(
    invitation: InvitationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.tenant_id:
        raise HTTPException(status_code=400, detail="User has no tenant")

    db_invitation = await crud.create(
        db=db, invitation=invitation, tenant_id=current_user.tenant_id
    )
    return db_invitation
