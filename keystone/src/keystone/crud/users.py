from sqlalchemy.ext.asyncio import AsyncSession

from src.keystone.models.invitation import Invitation
from src.keystone.models.user import User
from src.keystone.schemas.user import UserCreate


async def create_user_from_invitation(
    db: AsyncSession, *, invitation: Invitation, user_in: UserCreate
) -> User:
    db_user = User(
        email=user_in.email,
        tenant_id=invitation.tenant_id,
    )
    db_user.roles.append(invitation.role)
    invitation.status = "accepted"

    db.add(db_user)
    db.add(invitation)
    await db.commit()
    await db.refresh(db_user)
    return db_user
