from interfaces.protocols import IRepository
from models.entities import Account

class MemoryRepository(IRepository):
    def __init__(self):
        self._db: dict[int, Account] = {}

    def save(self, account: Account) -> None:
        self._db[account.account_id] = account

    def get(self, account_id: int) -> Account:
        if account_id not in self._db:
            raise ValueError(f"Счет {account_id} не найден")
        return self._db[account_id]