from dataclasses import dataclass

@dataclass
class Account:
    account_id: int
    balance: float = 0.0