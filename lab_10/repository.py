from models import Account
from exceptions import AccountNotFoundError

class AccountRepository:
    def __init__(self):
        self._db: dict[int, Account] = {}
        self._next_id = 1

    def get_all(self) -> list[Account]:
        return list(self._db.values())

    def get_by_id(self, acc_id: int) -> Account:
        if acc_id not in self._db:
            raise AccountNotFoundError(f"Счет {acc_id} не найден")
        return self._db[acc_id]

    def create(self, account_data: dict) -> Account:
        new_id = self._next_id
        account = Account(
            id=new_id,
            client_name=account_data["client_name"],
            currency=account_data["currency"],
            balance=account_data["balance"],
            status=account_data["status"]
        )
        self._db[new_id] = account
        self._next_id += 1
        return account

    def update(self, acc_id: int, account: Account) -> None:
        if acc_id not in self._db:
            raise AccountNotFoundError(f"Счет {acc_id} не найден")
        self._db[acc_id] = account

    def delete(self, acc_id: int) -> None:
        if acc_id not in self._db:
            raise AccountNotFoundError(f"Счет {acc_id} не найден")
        del self._db[acc_id]