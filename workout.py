import json

class Exercise:
    def __init__(self, name, category, sets, repetitions):
        self.name = name
        self.category = category
        self.sets = sets
        self.repetitions = repetitions

    def to_dict(self):
        return{
            "name": self.name,
            "category": self.category,
            "sets": self.sets,
            "repetitions": self.repetitions,
        }
    
    @staticmethod
    def from_dict(data):
        return Exercise(data["name"], data["category"], data["sets"], data["repetitions"])
    
class WorkoutPlan:
    def __init__(self):
        self.exercises = []

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def save_to_file(self):
       with open("Data_Workout.json", "w") as file:
            json.dump([exercise.to_dict() for exercise in self.exercises], file)

    def load_from_file(self):
        try:
            with open("Data_Workout.json", "r") as file:
                data = json.load(file)
                self.exercises = [Exercise.from_dict(item) for item in data]
        except FileNotFoundError:
            self.exercises = []