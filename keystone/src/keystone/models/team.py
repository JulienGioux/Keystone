import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.db import Base

class Team(Base):
    __tablename__ = "teams"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=True)
    parent = relationship("Team", remote_side=[id], back_populates="children")
    children = relationship("Team", back_populates="parent")
    memberships = relationship("TeamMembership", back_populates="team")

class TeamMembership(Base):
    __tablename__ = "team_memberships"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), primary_key=True)
    role = Column(String, nullable=False, default="member")  # e.g., 'member', 'manager'
    user = relationship("User", back_populates="team_memberships")
    team = relationship("Team", back_populates="memberships")
