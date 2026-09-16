def sport_generator(objects, target_sport):
    for obj in objects:
        if obj.sport_type.lower() == target_sport.lower():
            yield obj

class AthleteIterator:
    def __init__(self, objects):
        self.objects = objects
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.objects):
            raise StopIteration
        
        result = self.objects[self.index]
        self.index += 1
        return result