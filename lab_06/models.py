from dataclasses import dataclass, field
from enum import Enum
from typing import List

class AccountStatus(Enum):
    ACTIVE = "активен"
    BLOCKED = "заблокирован"
    CLOSED = "закрыт"

class BankError(Exception):
    pass

class AccountNotFoundError(BankError):
    pass

class InsufficientFundsError(BankError):
    pass

@dataclass
class Client:
    client_id: int
    name: str
    
    def get_report_data(self) -> str:
        return f"Клиент: {self.name} (ID: {self.client_id})"

@dataclass
class Operation:
    operation_id: int
    amount: float
    type: str

@dataclass
class Account:
    account_id: int
    client: Client
    balance: float = 0.0
    status: AccountStatus = AccountStatus.ACTIVE
    operations: List[Operation] = field(default_factory=list)
    
    def get_report_data(self) -> str:
        return f"Счёт {self.account_id}, Баланс: {self.balance} руб., Статус: {self.status.value}"