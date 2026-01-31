class FitnessPlan:
    def __init__(self, user):
        self.user = user
        self.bmi = None
        self.daily_calories = None

    def calculate_bmi(self):
        if not (self.user.weight and self.user.height):
            return None
        height_m = self.user.height / 100
        self.bmi = self.user.weight / (height_m ** 2)
        return round(self.bmi, 1)

    def calculate_calories(self):
        if not all([self.user.age, self.user.gender, self.user.weight,
                    self.user.height, self.user.activity_level]):
            return None

        # Mifflin-St Jeor BMR
        if self.user.gender.lower() == "male":
            bmr = 10 * self.user.weight + 6.25 * self.user.height - 5 * self.user.age + 5
        else:
            bmr = 10 * self.user.weight + 6.25 * self.user.height - 5 * self.user.age - 161

        multipliers = {"low": 1.2, "medium": 1.55, "high": 1.725}
        mult = multipliers.get(self.user.activity_level.lower(), 1.2)

        calories = bmr * mult

        goal_adj = {"lose": -500, "gain": +350, "maintain": 0}
        calories += goal_adj.get(self.user.goal.lower(), 0)

        self.daily_calories = round(calories)
        return self.daily_calories

    def get_workout_plan(self):
        plans = {
            "lose": [
                "30–40 min brisk walking or jogging",
                "20 min HIIT (burpees, mountain climbers, jump squats)",
                "3×12 bodyweight squats + lunges",
                "Plank 3×30–60 sec"
            ],
            "gain": [
                "Bench press 4×8–12",
                "Squats or leg press 4×8–12",
                "Pull-ups or lat pulldown 4×8–12",
                "Dumbbell rows 3×10–12",
                "Overhead press 3×10"
            ],
            "maintain": [
                "30 min yoga or mobility routine",
                "Full-body circuit (push-ups, rows, squats, planks)",
                "20–30 min cycling or swimming",
                "Daily 10 min stretching"
            ]
        }
        return plans.get(self.user.goal.lower(), ["Walk 30 min daily"])

    def get_meal_plan(self):
        plans = {
            "vegetarian": [
                "Breakfast: Greek yogurt + berries + granola",
                "Lunch: Chickpea salad with feta, veggies, olive oil",
                "Dinner: Lentil curry with brown rice & spinach",
                "Snack: Apple + peanut butter"
            ],
            "vegan": [
                "Breakfast: Oatmeal + peanut butter + banana + chia",
                "Lunch: Hummus wrap with veggies & avocado",
                "Dinner: Tofu stir-fry with broccoli & quinoa",
                "Snack: Handful almonds + orange"
            ],
            "non-vegetarian": [
                "Breakfast: 3 eggs omelette + spinach + whole grain toast",
                "Lunch: Grilled chicken breast + quinoa + broccoli",
                "Dinner: Salmon or lean beef + sweet potato + salad",
                "Snack: Greek yogurt or protein shake"
            ]
        }
        base = plans.get(self.user.diet_type.lower(), ["Balanced plate: protein + veggies + carbs"])
        base.append("💧 Drink 2.5–3.5 L water daily")
        return base