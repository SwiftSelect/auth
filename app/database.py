from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.models.users import User
from app.models.roles import Role
from app.models.actions import Action
from app.models.roles_actions_map import RoleActionMap
def init_db():
    Base.metadata.create_all(bind=engine)
init_db()
