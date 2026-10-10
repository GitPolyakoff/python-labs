from services.bank_service import BankCommandService, StatementService
from services.bank_service import DepositOperation, WithdrawOperation

class ConsoleUI:
    def __init__(self, command_service: BankCommandService, statement_service: StatementService):
        self.command = command_service
        self.statement = statement_service

    def run(self):
        print("1. Открыть счёт\n2. Пополнить\n3. Списать\n4. Выписка\n0. Выход")
        while True:
            choice = input("Выберите действие: ")
            try:
                if choice == "1":
                    acc_id = int(input("ID счёта: "))
                    self.command.open_account(acc_id)
                    print("Счёт открыт!")
                elif choice == "2":
                    acc_id = int(input("ID счёта: "))
                    amount = float(input("Сумма: "))
                    self.command.execute_operation(acc_id, DepositOperation(amount))
                    print("Счёт пополнен.")
                elif choice == "3":
                    acc_id = int(input("ID счёта: "))
                    amount = float(input("Сумма: "))
                    self.command.execute_operation(acc_id, WithdrawOperation(amount))
                    print("Средства списаны.")
                elif choice == "4":
                    acc_id = int(input("ID счёта: "))
                    print(self.statement.generate_statement(acc_id))
                elif choice == "0":
                    break
            except Exception as e:
                print(f"Ошибка: {e}")