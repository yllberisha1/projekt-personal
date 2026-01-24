from fastapi import FastAPI
from app.routes import auth_routes, fitness_routes, nutrition_routes
from app.database.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness + Nutrition Recommendation System")

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(fitness_routes.router, prefix="/fitness", tags=["Fitness"])
app.include_router(nutrition_routes.router, prefix="/nutrition", tags=["Nutrition"])
