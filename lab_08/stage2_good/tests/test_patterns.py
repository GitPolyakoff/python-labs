import unittest
from repositories.memory_repository import MemoryRepository
from factories.account_factory import AccountFactory
from strategies.fee_strategies import InterestStrategy, CommissionStrategy
from commands.bank_commands import DepositCommand, TransferCommand

class TestBankPatterns(unittest.TestCase):
    def setUp(self):
        self.repo = MemoryRepository()

    def test_factory_creates_correct_account(self):
        acc = AccountFactory.create(1, "депозит")
        self.assertEqual(acc.acc_type, "депозит")
        self.assertEqual(acc.account_id, 1)

    def test_factory_raises_error_for_invalid_type(self):
        with self.assertRaises(ValueError):
            AccountFactory.create(2, "неизвестный")

    def test_strategy_calculations(self):
        interest = InterestStrategy()
        commission = CommissionStrategy()
        
        self.assertEqual(interest.calculate(1000), 100)
        self.assertEqual(commission.calculate(1000), 50)

    def test_deposit_command(self):
        acc = AccountFactory.create(3, "текущий")
        self.repo.save(acc)
        
        cmd = DepositCommand(self.repo, 3, 2000)
        cmd.execute()
        
        self.assertEqual(self.repo.get(3).balance, 2000)

    def test_transfer_command(self):
        acc1 = AccountFactory.create(4, "текущий")
        acc2 = AccountFactory.create(5, "текущий")
        acc1.balance = 1000
        self.repo.save(acc1)
        self.repo.save(acc2)
        
        cmd = TransferCommand(self.repo, 4, 5, 400)
        cmd.execute()
        
        self.assertEqual(self.repo.get(4).balance, 600)
        self.assertEqual(self.repo.get(5).balance, 400)

if __name__ == "__main__":
    unittest.main()