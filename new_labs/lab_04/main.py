from services import SportsClubService
from exceptions import InvalidResultError

def main():
    service = SportsClubService()
    
    while True:
        print("\n===== Спортивный клуб =====")
        print("1. Добавить спортсмена")
        print("2. Показать всех спортсменов")
        print("3. Изменить результат")
        print("4. Поиск по виду спорта")
        print("5. Сортировка по результату")
        print("6. Статистика")
        print("7. Экспорт в CSV")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            try:
                name = input("Введите ФИО: ")
                age = int(input("Введите возраст: "))
                sport = input("Введите вид спорта: ")
                result = float(input("Введите результат: "))
                
                service.add_athlete(name, age, sport, result)
                print("Спортсмен успешно добавлен.")
            except ValueError:
                print("Ошибка: Возраст и результат должны быть числами.")
            except InvalidResultError as e:
                print(f"Ошибка данных: {e}")

        elif choice == '2':
            if not service.athletes:
                print("Список спортсменов пуст.")
            else:
                for i, a in enumerate(service.athletes, 1):
                    print(f"{i}. {a.full_name} ({a.age} лет) - {a.sport_type}: {a.result}")

        elif choice == '3':
            name = input("Введите ФИО спортсмена: ")
            try:
                new_result = float(input("Введите новый результат: "))
                if service.update_result(name, new_result):
                    print("Результат обновлен.")
                else:
                    print("Спортсмен не найден.")
            except ValueError:
                print("Ошибка: Результат должен быть числом.")
            except InvalidResultError as e:
                print(f"Ошибка данных: {e}")

        elif choice == '4':
            sport = input("Введите вид спорта для поиска: ")
            found = service.search_by_sport(sport)
            if found:
                for a in found:
                    print(f"- {a.full_name}: {a.result}")
            else:
                print("Спортсмены в данном виде спорта не найдены.")

        elif choice == '5':
            service.sort_by_result()
            print("Спортсмены отсортированы по результату.")

        elif choice == '6':
            stats = service.get_statistics()
            if stats:
                print(f"Всего спортсменов: {stats['count']}")
                print(f"Средний результат: {stats['average']:.2f}")
                print(f"Лучший результат: {stats['max']}")
                print(f"Худший результат: {stats['min']}")
            else:
                print("Нет данных для статистики.")

        elif choice == '7':
            service.export_to_csv()
            print("Данные успешно экспортированы в data.csv.")

        elif choice == '0':
            print("Завершение работы.")
            break
        else:
            print("Неверный ввод. Выберите номер из меню.")

if __name__ == "__main__":
    main()