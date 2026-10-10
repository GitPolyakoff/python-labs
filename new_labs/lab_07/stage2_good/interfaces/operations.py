from typing import Protocol
from models.entities import Account

class IOperation(Protocol):
    def execute(self, account: Account) -> None:
        ...