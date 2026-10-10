from exceptions import InvalidResultError

class Athlete:
    def __init__(self, full_name, age, sport_type, result):
        self.full_name = full_name
        self.age = age
        self.sport_type = sport_type
        self.result = result

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        if value < 0:
            raise InvalidResultError("Результат не может быть отрицательным.")
        self._result = value

    def to_dict(self):
        return {
            "full_name": self.full_name,
            "age": self.age,
            "sport_type": self.sport_type,
            "result": self.result
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["full_name"],
            data["age"],
            data["sport_type"],
            data["result"]
        )