class Athlete:
    """Базовый класс спортсмена."""
    def __init__(self, full_name, age, sport_type, result):
        self.full_name = full_name
        self.age = age
        self.sport_type = sport_type
        self.result = result

    def __str__(self):
        return f"{self.full_name} ({self.age} лет, {self.sport_type}) - Результат: {self.result}"

class Runner(Athlete):
    """Производный класс бегуна."""
    def __init__(self, full_name, age, result):
        super().__init__(full_name, age, "Бег", result)

class Swimmer(Athlete):
    """Производный класс пловца."""
    def __init__(self, full_name, age, result):
        super().__init__(full_name, age, "Плавание", result)