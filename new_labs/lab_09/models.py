from dataclasses import dataclass, asdict

@dataclass
class Delivery:
    id: int
    address: str
    courier_name: str
    status: str

    def to_dict(self):
        return asdict(self)