from pydantic import BaseModel

class FitnessInput(BaseModel):
    age: int
    height: float
    weight: float
    goal: str
