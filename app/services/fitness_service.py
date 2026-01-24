def generate_workout(goal):
    if goal == "lose":
        return ["Cardio", "HIIT", "Core"]
    elif goal == "gain":
        return ["Chest", "Back", "Legs"]
    return ["Full Body"]
