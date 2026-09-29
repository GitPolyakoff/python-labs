from interfaces.protocols import ICommand, IRepository

class DepositCommand(ICommand):
    def __init__(self, repo: IRepository, acc_id: int, amount: float):
        self.repo = repo
        self.acc_id = acc_id
        self.amount = amount

    def execute(self) -> None:
        acc = self.repo.get(self.acc_id)
        acc.balance += self.amount
        self.repo.save(acc)

class WithdrawCommand(ICommand):
    def __init__(self, repo: IRepository, acc_id: int, amount: float):
        self.repo = repo
        self.acc_id = acc_id
        self.amount = amount

    def execute(self) -> None:
        acc = self.repo.get(self.acc_id)
        if acc.balance < self.amount:
            raise ValueError("Недостаточно средств")
        acc.balance -= self.amount
        self.repo.save(acc)

class TransferCommand(ICommand):
    def __init__(self, repo: IRepository, from_id: int, to_id: int, amount: float):
        self.repo = repo
        self.from_id = from_id
        self.to_id = to_id
        self.amount = amount

    def execute(self) -> None:
        acc_from = self.repo.get(self.from_id)
        acc_to = self.repo.get(self.to_id)
        
        if acc_from.balance < self.amount:
            raise ValueError("Недостаточно средств для перевода")
            
        acc_from.balance -= self.amount
        acc_to.balance += self.amount
        
        self.repo.save(acc_from)
        self.repo.save(acc_to)