from typing import Protocol
from models.entities import Account

class IAccountReader(Protocol):
    def get(self, account_id: int) -> Account:
        ...

class IAccountWriter(Protocol):
    def save(self, account: Account) -> None:
        ...