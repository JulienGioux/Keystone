import secrets
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
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
    )
    db.add(db_invitation)
    await db.commit()
    await db.refresh(db_invitation)
    return db_invitation


async def get_by_token(db: AsyncSession, *, token: str) -> Invitation | None:
    statement = (
        select(Invitation)
        .where(Invitation.token == token)
        .where(Invitation.status == "pending")
        .where(Invitation.expires_at > datetime.now(timezone.utc))
    )
    result = await db.execute(statement)
    return result.scalar_one_or_none()
