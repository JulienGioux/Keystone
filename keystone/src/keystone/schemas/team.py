from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

class TeamCreate(BaseModel):
    name: str
    parent_id: Optional[UUID] = None

class Team(BaseModel):
    id: UUID
    name: str
    parent_id: Optional[UUID] = None
    tenant_id: UUID

    model_config = ConfigDict(from_attributes=True)

class TeamMemberCreate(BaseModel):
    user_id: UUID
    role: str

class TeamMember(BaseModel):
    user_id: UUID
    team_id: UUID
    role: str

    model_config = ConfigDict(from_attributes=True)
