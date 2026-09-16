from models import Runner, Swimmer
import operations as op
from generators import sport_generator, AthleteIterator
import sys

def main():
    athletes = []
    
    while True:
        print("\n===== МЕНЮ =====")
        print("1. Добавить спортсмена (ручной ввод)")
        print("2. Показать всех спортсменов (Собственный итератор)")
        print("3. Фильтрация по результату (filter + lambda)")
        print("4. Получение ФИО (map + lambda / comprehension)")
        print("5. Сортировка по результату (sorted + lambda)")
        print("6. Проверка наличия определенного возраста (any)")
        print("7. Запустить генератор по виду спорта (yield)")
        print("8. Демонстрация ленивых вычислений (Сравнение памяти)")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            print("\nКого вы хотите добавить?")
            print("1 - Бегун")
            print("2 - Пловец")
            sport_choice = input("Выберите тип (1 или 2): ")
            
            try:
                name = input("Введите ФИО: ")
                age = int(input("Введите возраст: "))
                result = float(input("Введите результат: "))
                
                if sport_choice == '1':
                    athletes.append(Runner(name, age, result))
                    print("Бегун успешно добавлен в базу!")
                elif sport_choice == '2':
                    athletes.append(Swimmer(name, age, result))
                    print("Пловец успешно добавлен в базу!")
                else:
                    print("Ошибка: неверный выбор типа спортсмена.")
            except ValueError:
                print("Ошибка: возраст и результат должны быть числами.")

        elif choice == '2':
            if not athletes:
                print("База спортсменов пока пуста. Сначала добавьте кого-нибудь.")
            else:
                print("\nВсе спортсмены (использование __next__):")
                iterator = AthleteIterator(athletes)
                for athlete in iterator:
                    print(athlete)
                
        elif choice == '3':
            if not athletes:
                print("База пуста.")
                continue
            try:
                min_result = float(input("Введите минимальный результат (например, 10.0): "))
                filtered = op.filter_objects(athletes, lambda a: a.result < min_result)
                print(f"\nСпортсмены с результатом меньше {min_result}:")
                for a in filtered:
                    print(a)
            except ValueError:
                print("Ошибка: введите число.")

        elif choice == '4':
            if not athletes:
                print("База пуста.")
                continue
            names_map = op.transform_objects(athletes, lambda a: a.full_name)
            print("\nФИО (через map):", names_map)
            
            names_comp = [a.full_name for a in athletes]
            print("ФИО (через comprehension):", names_comp)

        elif choice == '5':
            if not athletes:
                print("База пуста.")
                continue
            sorted_athletes = op.sort_objects(athletes, lambda a: a.result)
            print("\nСортировка (лучшие результаты сверху):")
            for a in sorted_athletes:
                print(a)
                
            if sorted_athletes:
                print(f"\nСамый лучший результат у: {sorted_athletes[0].full_name} ({sorted_athletes[0].result})")

        elif choice == '6':
            if not athletes:
                print("База пуста.")
                continue
            try:
                target_age = int(input("Введите искомый возраст: "))
                exists = op.check_condition_any(athletes, lambda a: a.age == target_age)
                if exists:
                    print(f"Да, спортсмены возраста {target_age} лет есть в базе.")
                else:
                    print(f"Нет, спортсменов возраста {target_age} лет не найдено.")
            except ValueError:
                print("Ошибка: введите целое число.")

        elif choice == '7':
            if not athletes:
                print("База пуста.")
                continue
            sport = input("Введите вид спорта (Бег/Плавание): ")
            print("\nГенератор выдает:")
            gen = sport_generator(athletes, sport)
            for a in gen:
                print(a)

        elif choice == '8':
            list_comp = [x * x for x in range(1_000_000)]
            gen_expr = (x * x for x in range(1_000_000))
            
            print(f"Размер списка в памяти: {sys.getsizeof(list_comp)} байт")
            print(f"Размер генератора в памяти: {sys.getsizeof(gen_expr)} байт")
            print("генератор использует ленивые вычисления и занимает минимум памяти, "
                  "так как не генерирует все числа сразу.")

        elif choice == '0':
            print("Завершение работы.")
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()