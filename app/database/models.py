from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.db import Base

class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)

class FitnessProfileTable(Base):
    __tablename__ = "fitness_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    goal = Column(String)
