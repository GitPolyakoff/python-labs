from dataclasses import dataclass, asdict

@dataclass
class Account:
    id: int
    client_name: str
    currency: str
    balance: float
    status: str

    def to_dict(self):
        return asdict(self)