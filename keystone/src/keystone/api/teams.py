from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.keystone.api.dependencies import get_current_user, get_db
from src.keystone.crud import teams as teams_crud
from src.keystone.models.team import Team as TeamModel
from src.keystone.models.user import User
from src.keystone.schemas.team import Team, TeamCreate, TeamMember, TeamMemberCreate

router = APIRouter()


@router.get("/", response_model=List[Team])
async def list_teams(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    teams = await teams_crud.get_multi_by_tenant(
        db, tenant_id=current_user.tenant_id
    )
    return teams


@router.post("/", response_model=Team, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_in: TeamCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if "Administrateur" not in [role.name for role in current_user.roles]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create a team.",
        )

    team = await teams_crud.create(
        db, team_in=team_in, tenant_id=current_user.tenant_id
    )
    return team


@router.post(
    "/{team_id}/members",
    response_model=TeamMember,
    status_code=status.HTTP_201_CREATED,
)
async def add_team_member(
    team_id: UUID,
    member_in: TeamMemberCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    team = await db.get(TeamModel, team_id)
    if not team or team.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )

    if "Administrateur" not in [role.name for role in current_user.roles]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to add a member to this team.",
        )

    if member_in.role not in ["member", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid role. Must be 'member' or 'manager'.",
        )

    user_to_add = await db.get(User, member_in.user_id)
    if not user_to_add:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    membership = await teams_crud.add_member(db, team=team, member_in=member_in)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this team.",
        )
    return membership
