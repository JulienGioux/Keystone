from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class InvitationCreate(BaseModel):
    email: EmailStr
    role_id: UUID


class InvitationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: EmailStr
    status: str
    expires_at: datetime
    role_id: UUID
    tenant_id: UUID
