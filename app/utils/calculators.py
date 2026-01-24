def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

def daily_calories(goal):
    if goal == "lose":
        return 1800
    elif goal == "gain":
        return 2800
    return 2200
