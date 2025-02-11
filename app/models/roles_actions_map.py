from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import relationship
from app.database import Base

class RoleActionMap(Base):
    __tablename__ = "roles_actions_map"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    action_name = Column(String, ForeignKey("actions.name"), primary_key=True)

    role = relationship("Role", back_populates="role_actions")
    action = relationship("Action", back_populates="role_actions")

    __table_args__ = (UniqueConstraint("role_id", "action_name", name="unique_role_action"),)
