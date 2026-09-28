import inspect
from models import Account, Client, Operation, AccountStatus, AccountNotFoundError, InsufficientFundsError
from protocols import Reportable
from decorators import log_call, measure_time

class BankService:
    def __init__(self):
        self.accounts: list[Account] = []
        self.clients: list[Client] = []
        self.op_counter = 1

    def add_account(self, account: Account):
        self.accounts.append(account)

    def find_account(self, account_id: int) -> Account | None:
        for acc in self.accounts:
            if acc.account_id == account_id:
                return acc
        return None

    @log_call
    def deposit(self, account_id: int, amount: float):
        acc = self.find_account(account_id)
        if not acc:
            raise AccountNotFoundError("Счёт не найден.")
        if acc.status != AccountStatus.ACTIVE:
            raise ValueError("Операция отклонена: счёт не активен.")
        
        acc.balance += amount
        op = Operation(self.op_counter, amount, "пополнение")
        acc.operations.append(op)
        self.op_counter += 1

    @log_call
    def withdraw(self, account_id: int, amount: float):
        acc = self.find_account(account_id)
        if not acc:
            raise AccountNotFoundError("Счёт не найден.")
        if acc.status != AccountStatus.ACTIVE:
            raise ValueError("Операция отклонена: счёт не активен.")
        if acc.balance < amount:
            raise InsufficientFundsError("Недостаточно средств на счёте.")
        
        acc.balance -= amount
        op = Operation(self.op_counter, amount, "списание")
        acc.operations.append(op)
        self.op_counter += 1

    def calculate_turnover(self, account_id: int) -> float:
        acc = self.find_account(account_id)
        if not acc:
            raise AccountNotFoundError("Счёт не найден.")
        return sum(op.amount for op in acc.operations)

    @measure_time
    def get_statistics(self) -> dict:
        total_accs = len(self.accounts)
        active_accs = len([a for a in self.accounts if a.status == AccountStatus.ACTIVE])
        total_money = sum(a.balance for a in self.accounts)
        return {
            "Всего счетов": total_accs,
            "Активных счетов": active_accs,
            "Сумма денег в банке": total_money
        }

def print_report(item: Reportable):
    print(f"Печать через Protocol: {item.get_report_data()}")

def inspect_object(obj):
    print("\n=== ИНФОРМАЦИЯ ОБ ОБЪЕКТЕ ===")
    print(f"1. Тип объекта (type): {type(obj)}")
    print(f"2. Принадлежит ли классу Account (isinstance): {isinstance(obj, Account)}")
    
    if hasattr(obj, "balance"):
        print(f"3. Значение баланса (getattr): {getattr(obj, 'balance')}")
    
    attributes = [m[0] for m in inspect.getmembers(obj) if not m[0].startswith('_')]
    print(f"4. Атрибуты и методы (inspect.getmembers): {attributes}")