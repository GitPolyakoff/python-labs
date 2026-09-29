from models.entities import Account

class AccountFactory:
    @staticmethod
    def create(account_id: int, acc_type: str) -> Account:
        valid_types = ["текущий", "накопительный", "депозит"]
        if acc_type not in valid_types:
            raise ValueError(f"Неизвестный тип счета: {acc_type}")
        return Account(account_id=account_id, acc_type=acc_type)