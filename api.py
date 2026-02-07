# api.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from database import engine, get_db, Base
from models import UserDB, UserCreate, UserUpdate, UserOut
from fitness_app.fitness_plan import FitnessPlan

app = FastAPI(title="Fitness Recommendation API")


Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = UserDB(username=user.username, password=user.password)  # hash in production!
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user or user.password != password:  # compare hashed in prod
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": user.username}


@app.get("/user/{username}", response_model=UserOut)
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/user/{username}", response_model=UserOut)
def update_user(username: str, update_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@app.post("/generate_plan/{username}")
def generate_plan(username: str, db: Session = Depends(get_db)):
    user_db = db.query(UserDB).filter(UserDB.username == username).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")


    from user import User
    user = User(
        username=user_db.username,
        password="",
        age=user_db.age,
        gender=user_db.gender,
        weight=user_db.weight,
        height=user_db.height,
        goal=user_db.goal,
        diet_type=user_db.diet_type,
        activity_level=user_db.activity_level
    )

    plan = FitnessPlan(user)
    bmi = plan.calculate_bmi()
    calories = plan.calculate_calories()
    workouts = plan.get_workout_plan()
    meals = plan.get_meal_plan()

    return {
        "bmi": bmi,
        "daily_calories": calories,
        "workouts": workouts,
        "meals": meals
    }



if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)