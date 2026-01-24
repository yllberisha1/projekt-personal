from fastapi import APIRouter
from app.schemas.fitness_schema import FitnessInput
from app.services.nutrition_service import generate_meals
from app.utils.calculators import daily_calories

router = APIRouter()

@router.post("/recommend")
def recommend_nutrition(data: FitnessInput):
    calories = daily_calories(data.goal)
    meals = generate_meals(calories)
    return meals
