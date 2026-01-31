import json

class User:
    def __init__(self, username, password, age=None, gender=None, weight=None, height=None,
                 goal=None, diet_type=None, activity_level=None):
        self.username = username
        self.password = password  # WARNING: in production → hash this!
        self.age = age
        self.gender = gender
        self.weight = weight      # kg
        self.height = height      # cm
        self.goal = goal          # "lose", "gain", "maintain"
        self.diet_type = diet_type
        self.activity_level = activity_level

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "age": self.age,
            "gender": self.gender,
            "weight": self.weight,
            "height": self.height,
            "goal": self.goal,
            "diet_type": self.diet_type,
            "activity_level": self.activity_level
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data["username"],
            password=data["password"],
            age=data.get("age"),
            gender=data.get("gender"),
            weight=data.get("weight"),
            height=data.get("height"),
            goal=data.get("goal"),
            diet_type=data.get("diet_type"),
            activity_level=data.get("activity_level")
        )