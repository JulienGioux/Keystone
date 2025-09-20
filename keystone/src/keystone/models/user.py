import uuid
from sqlalchemy import Column, String, ForeignKey, Table, Uuid
from sqlalchemy.orm import relationship
from ..core.db import Base

user_role_association = Table(
    "user_role_association",
    Base.metadata,
    Column("user_id", Uuid, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Uuid, ForeignKey("roles.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    tenant_id = Column(Uuid, ForeignKey("tenants.id"), nullable=False)
    tenant = relationship("Tenant", back_populates="users")
    roles = relationship("Role", secondary=user_role_association)
