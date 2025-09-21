from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.keystone.api.dependencies import get_current_user, get_db
from src.keystone.crud import invitations as crud
from src.keystone.models.user import User
from src.keystone.schemas.invitation import InvitationCreate, InvitationRead

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
