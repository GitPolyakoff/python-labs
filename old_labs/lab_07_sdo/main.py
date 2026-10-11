class Animal:
    # Приватная переменная для хранения единственного экземпляра класса
    __instance = None

    def __new__(cls, *args, **kwargs):
        # Если экземпляр еще не создан, выделяем для него память
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, name="Безымянный"):
        # Проверяем, есть ли уже у объекта имя
        if not hasattr(self, 'name_animal'):
            self.name_animal = name
            self.age_animal = 1

    def eat(self):
        print(self.name_animal + " ест...")

    def sleep(self):
        print(self.name_animal + " спит, ему " + str(self.age_animal) + " год(а).")

cat1 = Animal("Барсик")
print("Создан первый объект:")
cat1.eat()

cat2 = Animal("Мурзик")

print("\nПытаемся создать второй объект, но получаем первого:")
cat2.eat() 

cat2.age_animal = 5

print("\nПроверяем возраст у первого объекта (cat1):")
cat1.sleep()

print("\ncat1 и cat2 - это один и тот же объект?", cat1 is cat2)