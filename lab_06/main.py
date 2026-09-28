from models import Client, Account, AccountStatus, AccountNotFoundError, InsufficientFundsError
from services import BankService, print_report, inspect_object
from context import transaction_context
from decorators import repeat

@repeat(2)
def welcome_message():
    print("Добро пожаловать в систему управления банком!")

def main():
    bank = BankService()
    welcome_message()

    while True:
        print("\n--- ГЛАВНОЕ МЕНЮ ---")
        print("1. Добавить счёт")
        print("2. Пополнить счёт")
        print("3. Списать средства")
        print("4. Изменить статус счёта")
        print("5. Расчёт оборота")
        print("6. Вывести все счета")
        print("7. Получить статистику")
        print("8. Демонстрация Protocol")
        print("9. Интроспекция объекта")
        print("10. Демонстрация контекстного менеджера")
        print("0. Выход")
        
        choice = input("Выберите пункт меню: ")
        
        try:
            if choice == "1":
                acc_id = int(input("Введите ID счёта (число): "))
                name = input("Введите имя клиента: ")
                client = Client(client_id=len(bank.clients)+1, name=name)
                bank.clients.append(client)
                bank.add_account(Account(account_id=acc_id, client=client))
                print("Счёт успешно добавлен!")
            
            elif choice == "2":
                acc_id = int(input("Введите ID счёта: "))
                amount = float(input("Введите сумму пополнения: "))
                bank.deposit(acc_id, amount)
            
            elif choice == "3":
                acc_id = int(input("Введите ID счёта: "))
                amount = float(input("Введите сумму списания: "))
                bank.withdraw(acc_id, amount)
            
            elif choice == "4":
                acc_id = int(input("Введите ID счёта: "))
                print("1 - Активен, 2 - Заблокирован, 3 - Закрыт")
                st_choice = input("Выберите новый статус: ")
                acc = bank.find_account(acc_id)
                if not acc:
                    raise AccountNotFoundError("Счёт не найден.")
                
                if st_choice == "1": acc.status = AccountStatus.ACTIVE
                elif st_choice == "2": acc.status = AccountStatus.BLOCKED
                elif st_choice == "3": acc.status = AccountStatus.CLOSED
                else: print("Неверный выбор статуса.")
                print(f"Статус изменён на: {acc.status.value}")
            
            elif choice == "5":
                acc_id = int(input("Введите ID счёта: "))
                turnover = bank.calculate_turnover(acc_id)
                print(f"Общий оборот по счёту: {turnover} руб.")
            
            elif choice == "6":
                if not bank.accounts:
                    print("Список счетов пуст.")
                for acc in bank.accounts:
                    print(f"Счёт {acc.account_id} | Клиент: {acc.client.name} | Баланс: {acc.balance} | Статус: {acc.status.value}")
            
            elif choice == "7":
                stats = bank.get_statistics()
                for key, value in stats.items():
                    print(f"{key}: {value}")
                    
            elif choice == "8":
                if bank.accounts:
                    acc = bank.accounts[0]
                    print_report(acc.client)
                    print_report(acc)
                else:
                    print("Сначала добавьте хотя бы один счёт.")
                    
            elif choice == "9":
                if bank.accounts:
                    inspect_object(bank.accounts[0])
                else:
                    print("Сначала добавьте счёт.")
                    
            elif choice == "10":
                if bank.accounts:
                    acc_id = bank.accounts[0].account_id
                    with transaction_context(acc_id):
                        bank.deposit(acc_id, 100)
                else:
                    print("Добавьте счёт для демонстрации транзакции.")
            
            elif choice == "0":
                print("Выход из программы.")
                break
            else:
                print("Неизвестная команда.")
                
        except ValueError as e:
            print(f"Ошибка ввода данных: {e}")
        except AccountNotFoundError as e:
            print(f"Ошибка поиска: {e}")
        except InsufficientFundsError as e:
            print(f"Финансовая ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()