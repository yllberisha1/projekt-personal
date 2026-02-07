# models.py
from sqlalchemy import Column, Integer, String, Float
from database import Base
from pydantic import BaseModel

# ── SQLAlchemy model (for database) ──
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    goal = Column(String, nullable=True)
    diet_type = Column(String, nullable=True)
    activity_level = Column(String, nullable=True)


class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    age: int | None = None
    gender: str | None = None
    weight: float | None = None
    height: float | None = None
    goal: str | None = None
    diet_type: str | None = None
    activity_level: str | None = None

class UserOut(BaseModel):
    username: str
    age: int | None
    gender: str | None
    weight: float | None
    height: float | None
    goal: str | None
    diet_type: str | None
    activity_level: str | None

    class Config:
        from_attributes = True