from interfaces.repository import IAccountReader, IAccountWriter
from interfaces.operations import IOperation
from models.entities import Account

class BankCommandService:
    """Сервис для изменения данных (запись). Зависит только от IAccountWriter и IAccountReader."""
    def __init__(self, writer: IAccountWriter, reader: IAccountReader):
        self.writer = writer
        self.reader = reader

    def open_account(self, account_id: int) -> None:
        acc = Account(account_id=account_id)
        self.writer.save(acc)

    def execute_operation(self, account_id: int, operation: IOperation) -> None:
        acc = self.reader.get(account_id)
        operation.execute(acc)
        self.writer.save(acc)

class StatementService:
    """Сервис для чтения данных (выписка). Зависит только от IAccountReader."""
    def __init__(self, reader: IAccountReader):
        self.reader = reader

    def generate_statement(self, account_id: int) -> str:
        acc = self.reader.get(account_id)
        return f"Выписка по счёту {acc.account_id} | Текущий баланс: {acc.balance} руб."

class DepositOperation:
    def __init__(self, amount: float):
        self.amount = amount
    def execute(self, account: Account) -> None:
        account.balance += self.amount

class WithdrawOperation:
    def __init__(self, amount: float):
        self.amount = amount
    def execute(self, account: Account) -> None:
        if account.balance < self.amount:
            raise ValueError("Недостаточно средств")
        account.balance -= self.amount