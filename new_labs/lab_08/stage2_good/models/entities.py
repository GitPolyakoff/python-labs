from dataclasses import dataclass

@dataclass
class Account:
    account_id: int
    acc_type: str
    balance: float = 0.0