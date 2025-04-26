from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Org(Base):
    __tablename__ = "orgs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    size = Column(String, nullable=True, default="100-500 employees")
    industry = Column(String, nullable=True, default="Technology")
    users = relationship("User", back_populates="org")