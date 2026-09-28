from interfaces.repository import IAccountReader, IAccountWriter
from models.entities import Account

class MemoryAccountRepository(IAccountReader, IAccountWriter):
    def __init__(self):
        self._storage: dict[int, Account] = {}

    def save(self, account: Account) -> None:
        self._storage[account.account_id] = account

    def get(self, account_id: int) -> Account:
        if account_id not in self._storage:
            raise ValueError("Счёт не найден")
        return self._storage[account_id]