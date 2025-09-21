from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.keystone.models.invitation import Invitation
from src.keystone.schemas.invitation import InvitationCreate


async def create(
    db: AsyncSession, invitation: InvitationCreate, tenant_id: UUID
) -> Invitation:
    db_invitation = Invitation(
        email=invitation.email,
        role_id=invitation.role_id,
        tenant_id=tenant_id,
    )
    db.add(db_invitation)
    await db.commit()
    await db.refresh(db_invitation)
    return db_invitation
