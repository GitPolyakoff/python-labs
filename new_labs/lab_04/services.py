from models import Athlete
import storage

class SportsClubService:
    def __init__(self):
        self.athletes = []
        self.load_data()

    def load_data(self):
        raw_data = storage.load_json()
        self.athletes = [Athlete.from_dict(item) for item in raw_data]

    def save_data(self):
        raw_data = [a.to_dict() for a in self.athletes]
        storage.save_json(raw_data)

    def export_to_csv(self):
        raw_data = [a.to_dict() for a in self.athletes]
        storage.export_csv(raw_data)

    def add_athlete(self, full_name, age, sport_type, result):
        athlete = Athlete(full_name, age, sport_type, result)
        self.athletes.append(athlete)
        self.save_data()

    def update_result(self, full_name, new_result):
        for athlete in self.athletes:
            if athlete.full_name.lower() == full_name.lower():
                athlete.result = new_result
                self.save_data()
                return True
        return False

    def search_by_sport(self, sport_type):
        return [a for a in self.athletes if a.sport_type.lower() == sport_type.lower()]

    def sort_by_result(self):
        self.athletes.sort(key=lambda x: x.result, reverse=True)
        self.save_data()

    def get_statistics(self):
        if not self.athletes:
            return None
        
        results = [a.result for a in self.athletes]
        return {
            "count": len(results),
            "average": sum(results) / len(results),
            "max": max(results),
            "min": min(results)
        }