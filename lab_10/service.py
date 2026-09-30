from repository import AccountRepository
from schemas import validate_account_data
from models import Account

class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repo = repository

    def get_accounts(self, status: str = None, currency: str = None, sort_by: str = None, order: str = "asc") -> list[dict]:
        accounts = self.repo.get_all()
        
        if status:
            accounts = [a for a in accounts if a.status == status]
        if currency:
            accounts = [a for a in accounts if a.currency == currency]
            
        if sort_by == "balance":
            accounts.sort(key=lambda x: x.balance, reverse=(order == "desc"))
        elif sort_by == "client_name":
            accounts.sort(key=lambda x: x.client_name, reverse=(order == "desc"))
            
        return [a.to_dict() for a in accounts]

    def get_account(self, acc_id: int) -> dict:
        return self.repo.get_by_id(acc_id).to_dict()

    def create_account(self, data: dict) -> dict:
        validate_account_data(data)
        return self.repo.create(data).to_dict()

    def update_account_full(self, acc_id: int, data: dict) -> dict:
        validate_account_data(data)
        acc = self.repo.get_by_id(acc_id)
        acc.client_name = data["client_name"]
        acc.currency = data["currency"]
        acc.balance = data["balance"]
        acc.status = data["status"]
        self.repo.update(acc_id, acc)
        return acc.to_dict()

    def update_account_partial(self, acc_id: int, data: dict) -> dict:
        validate_account_data(data, partial=True)
        acc = self.repo.get_by_id(acc_id)
        if "client_name" in data: acc.client_name = data["client_name"]
        if "currency" in data: acc.currency = data["currency"]
        if "balance" in data: acc.balance = data["balance"]
        if "status" in data: acc.status = data["status"]
        self.repo.update(acc_id, acc)
        return acc.to_dict()

    def delete_account(self, acc_id: int) -> None:
        self.repo.delete(acc_id)

    def calculate_total_funds(self) -> dict:
        accounts = self.repo.get_all()
        total = sum(a.balance for a in accounts if a.status == "active")
        return {"total_active_funds": total, "accounts_counted": len([a for a in accounts if a.status == "active"])}