from fastapi import APIRouter
from app.schemas.fitness_schema import FitnessInput
from app.services.fitness_service import generate_workout
from app.utils.calculators import calculate_bmi

router = APIRouter()

@router.post("/recommend")
def recommend_fitness(data: FitnessInput):
    bmi = calculate_bmi(data.weight, data.height)
    workout = generate_workout(data.goal)
    return {"BMI": bmi, "Workout Plan": workout}
