from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.keystone.models.team import Team, TeamMembership
from src.keystone.schemas.team import TeamCreate, TeamMemberCreate

async def create(db: AsyncSession, *, team_in: TeamCreate, tenant_id: UUID) -> Team:
    db_team = Team(**team_in.model_dump(), tenant_id=tenant_id)
    db.add(db_team)
    await db.commit()
    await db.refresh(db_team)
    return db_team

async def get_multi_by_tenant(db: AsyncSession, *, tenant_id: UUID) -> list[Team]:
    statement = select(Team).where(Team.tenant_id == tenant_id)
    result = await db.execute(statement)
    return result.scalars().all()

async def add_member(db: AsyncSession, *, team: Team, member_in: TeamMemberCreate) -> TeamMembership:
    # Check if user is already a member
    statement = select(TeamMembership).where(
        TeamMembership.team_id == team.id,
        TeamMembership.user_id == member_in.user_id,
    )
    result = await db.execute(statement)
    if result.scalar_one_or_none():
        return None

    membership = TeamMembership(
        team_id=team.id,
        user_id=member_in.user_id,
        role=member_in.role,
    )
    db.add(membership)
    await db.commit()
    await db.refresh(membership)
    return membership
