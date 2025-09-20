import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.keystone.models.invitation import Invitation
from src.keystone.schemas.invitation import InvitationCreate


async def create(
    db: AsyncSession, invitation: InvitationCreate, tenant_id: UUID
) -> Invitation:
    token = secrets.token_urlsafe(32)
    db_invitation = Invitation(
        email=invitation.email,
        role_id=invitation.role_id,
        tenant_id=tenant_id,
        token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    db.add(db_invitation)
    await db.commit()
    await db.refresh(db_invitation)
    return db_invitation
