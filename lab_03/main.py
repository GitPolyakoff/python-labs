class MedicalWorker:
    def __init__(self, name, experience):
        self.name = name
        self._experience = experience

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        if value < 0:
            print("Ошибка: стаж не может быть отрицательным.")
        else:
            self._experience = value

    def get_info(self):
        return f"Сотрудник: {self.name}, стаж: {self.experience} лет."

class Doctor(MedicalWorker):
    def __init__(self, name, experience, specialization):
        super().__init__(name, experience)
        self.specialization = specialization

    def get_info(self):
        return f"Врач: {self.name}, специализация: {self.specialization}, стаж: {self.experience} лет."

class Nurse(MedicalWorker):
    def __init__(self, name, experience, category):
        super().__init__(name, experience)
        self.category = category

    def get_info(self):
        return f"Медсестра: {self.name}, категория: {self.category}, стаж: {self.experience} лет."

class MedicalCenter:
    def __init__(self, name):
        self.name = name
        self.workers = []

    def add_worker(self, worker):
        self.workers.append(worker)
        print("Сотрудник успешно добавлен!")

    def show_all_workers(self):
        if not self.workers:
            print("В центре пока нет сотрудников.")
            return
        
        print(f"\n--- Сотрудники центра '{self.name}' ---")
        for worker in self.workers:
            print(worker.get_info())

    def update_experience(self, name, new_experience):
        for worker in self.workers:
            if worker.name == name:
                worker.experience = new_experience
                print(f"Стаж сотрудника {name} обновлен.")
                return
        print("Сотрудник с таким именем не найден.")

    def fire_worker(self, name):
        for worker in self.workers:
            if worker.name == name:
                self.workers.remove(worker)
                print(f"Сотрудник {name} уволен (удален из базы).")
                return
        print("Сотрудник с таким именем не найден.")

    def show_statistics(self):
        if not self.workers:
            print("Нет данных для статистики.")
            return
        
        total_exp = sum(worker.experience for worker in self.workers)
        avg_exp = total_exp / len(self.workers)
        print(f"\n--- Статистика центра ---")
        print(f"Всего сотрудников: {len(self.workers)}")
        print(f"Средний стаж персонала: {avg_exp:.1f} лет")

    def perform_action(self):
        if not self.workers:
            print("Некому работать, наймите сотрудников!")
            return
        print("\nМедицинский центр начинает прием пациентов...")
        print("Все сотрудники приступили к своим обязанностям.")

def main():
    center = MedicalCenter("Здоровье")
    
    while True:
        print("\n===== МЕНЮ =====")
        print("1. Создать объект (Нанять сотрудника)")
        print("2. Показать объекты (Список сотрудников)")
        print("3. Выполнить действие (Начать прием пациентов)")
        print("4. Изменить объект (Обновить стаж)")
        print("5. Удалить объект (Уволить сотрудника)")
        print("6. Показать статистику")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            type_choice = input("Кого нанять? (1 - Врач, 2 - Медсестра): ")
            name = input("Введите имя: ")
            exp = int(input("Введите стаж: "))
            
            if type_choice == '1':
                spec = input("Введите специализацию: ")
                center.add_worker(Doctor(name, exp, spec))
            elif type_choice == '2':
                cat = input("Введите категорию: ")
                center.add_worker(Nurse(name, exp, cat))
            else:
                print("Неверный тип сотрудника.")
                
        elif choice == '2':
            center.show_all_workers()
            
        elif choice == '3':
            center.perform_action()
            
        elif choice == '4':
            name = input("Введите имя сотрудника: ")
            new_exp = int(input("Введите новый стаж: "))
            center.update_experience(name, new_exp)
            
        elif choice == '5':
            name = input("Введите имя сотрудника для увольнения: ")
            center.fire_worker(name)
            
        elif choice == '6':
            center.show_statistics()
            
        elif choice == '0':
            print("Завершение работы.")
            break
        else:
            print("Неверный ввод. Выберите номер из меню.")

if __name__ == "__main__":
    main()