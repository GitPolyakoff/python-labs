class Account:
    def __init__(self, account_id: int, acc_type: str):
        self.account_id = account_id
        self.acc_type = acc_type
        self.balance = 0.0

class BadBankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_id: int, acc_type: str):
        if acc_type in ["текущий", "накопительный", "депозит"]:
            self.accounts[account_id] = Account(account_id, acc_type)
        else:
            raise ValueError("Неизвестный тип счета")

    def execute_operation(self, command_type: str, acc_id: int, amount: float = 0, target_id: int = None):
        acc = self.accounts.get(acc_id)
        if not acc:
            raise ValueError("Счет не найден")

        if command_type == "пополнение":
            acc.balance += amount
        elif command_type == "снятие":
            acc.balance -= amount
        elif command_type == "перевод":
            target_acc = self.accounts.get(target_id)
            if target_acc:
                acc.balance -= amount
                target_acc.balance += amount
        else:
            raise ValueError("Неизвестная операция")

    def calculate_fee(self, acc_id: int, amount: float, calc_type: str) -> float:
        if calc_type == "комиссия":
            return amount * 0.05
        elif calc_type == "проценты":
            return amount * 0.10
        elif calc_type == "льготный":
            return amount * 0.01
        else:
            return 0.0

if __name__ == "__main__":
    bank = BadBankSystem()
    bank.create_account(1, "текущий")
    bank.execute_operation("пополнение", 1, 1000)
    print(f"Баланс: {bank.accounts[1].balance}")
    print(f"Комиссия с 1000: {bank.calculate_fee(1, 1000, 'комиссия')}")