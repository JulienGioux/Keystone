import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: uuid.UUID
    email: EmailStr
    tenant_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
