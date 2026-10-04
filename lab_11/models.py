from dataclasses import dataclass

@dataclass
class Account:
    id: int
    client_id: int
    balance: float
    status: str