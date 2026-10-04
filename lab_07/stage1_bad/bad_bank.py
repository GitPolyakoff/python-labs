class Account:
    def __init__(self, account_id: int, balance: float):
        self.account_id = account_id
        self.balance = balance

class DepositOnlyAccount(Account):
    def withdraw(self, amount: float):
        raise Exception("С этого счета нельзя списывать средства!")

#нарушен принцип единственной ответственности и логика и консоль всё в куче
#нарушен принцип инверсии зависимостей жесткая зависимость от print и бд
class BankSystem:
    def __init__(self):
        self.database = {} #бд внутри класса

    def open_account(self, account_id: int):
        self.database[account_id] = Account(account_id, 0.0)
        print(f"Счет {account_id} открыт.")

    #нарушен принцип открытости закрытости, при добавлении новой операции придется лезть в метод
    def process_operation(self, op_type: str, account_id: int, amount: float):
        acc = self.database.get(account_id)
        if op_type == "deposit":
            acc.balance += amount
        elif op_type == "withdraw":
            acc.balance -= amount
        else:
            print("Неизвестная операция")

    #нарушен принцип разделения интерфейсов один класс для чтения и записи
    def print_statement(self, account_id: int):
        acc = self.database.get(account_id)
        print(f"Выписка: Счет {acc.account_id}, Баланс: {acc.balance}")

if __name__ == "__main__":
    bank = BankSystem()
    bank.open_account(1)
    bank.process_operation("deposit", 1, 1000)
    bank.print_statement(1)