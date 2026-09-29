from factories.account_factory import AccountFactory
from commands.bank_commands import DepositCommand, WithdrawCommand, TransferCommand
from strategies.fee_strategies import CommissionStrategy, PreferentialStrategy, InterestStrategy
from interfaces.protocols import IRepository

class ConsoleUI:
    def __init__(self, repo: IRepository):
        self.repo = repo
        self.strategies = {
            "1": ("Стандартная комиссия", CommissionStrategy()),
            "2": ("Льготная комиссия", PreferentialStrategy()),
            "3": ("Расчет процентов", InterestStrategy())
        }

    def run(self):
        while True:
            print("\n--- БАНКОВСКАЯ СИСТЕМА ---")
            print("1. Открыть счет (Factory)")
            print("2. Пополнить счет (Command)")
            print("3. Снять деньги (Command)")
            print("4. Перевод между счетами (Command)")
            print("5. Расчет комиссии/процентов (Strategy)")
            print("6. Вывести баланс")
            print("0. Выход")
            
            choice = input("Выберите действие: ")
            
            try:
                if choice == "1":
                    acc_id = int(input("ID счета: "))
                    acc_type = input("Тип (текущий/накопительный/депозит): ")
                    acc = AccountFactory.create(acc_id, acc_type)
                    self.repo.save(acc)
                    print(f"Счет {acc_id} успешно открыт!")
                    
                elif choice == "2":
                    acc_id = int(input("ID счета: "))
                    amount = float(input("Сумма пополнения: "))
                    cmd = DepositCommand(self.repo, acc_id, amount)
                    cmd.execute()
                    print("Успешно пополнено.")
                    
                elif choice == "3":
                    acc_id = int(input("ID счета: "))
                    amount = float(input("Сумма снятия: "))
                    cmd = WithdrawCommand(self.repo, acc_id, amount)
                    cmd.execute()
                    print("Успешно снято.")
                    
                elif choice == "4":
                    from_id = int(input("Откуда (ID): "))
                    to_id = int(input("Куда (ID): "))
                    amount = float(input("Сумма перевода: "))
                    cmd = TransferCommand(self.repo, from_id, to_id, amount)
                    cmd.execute()
                    print("Успешно переведено.")
                    
                elif choice == "5":
                    acc_id = int(input("ID счета: "))
                    acc = self.repo.get(acc_id)
                    print("1 - Стандартная (5%), 2 - Льготная (1%), 3 - Проценты (10%)")
                    strat_choice = input("Выберите алгоритм: ")
                    
                    if strat_choice in self.strategies:
                        name, strategy = self.strategies[strat_choice]
                        fee = strategy.calculate(acc.balance)
                        print(f"Результат ({name}) от баланса {acc.balance}: {fee} руб.")
                    else:
                        print("Неверный выбор алгоритма.")
                        
                elif choice == "6":
                    acc_id = int(input("ID счета: "))
                    acc = self.repo.get(acc_id)
                    print(f"Баланс счета {acc_id} ({acc.acc_type}): {acc.balance} руб.")
                    
                elif choice == "0":
                    break
                else:
                    print("Неизвестная команда")
                    
            except Exception as e:
                print(f"Ошибка: {e}")