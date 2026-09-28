import unittest
from repositories.memory_repository import MemoryAccountRepository
from services.bank_service import BankCommandService, StatementService
from services.bank_service import DepositOperation, WithdrawOperation

class TestBankBusinessLogic(unittest.TestCase):
    def setUp(self):
        self.repo = MemoryAccountRepository()
        self.command_service = BankCommandService(self.repo, self.repo)
        self.statement_service = StatementService(self.repo)

    def test_open_account(self):
        self.command_service.open_account(101)
        acc = self.repo.get(101)
        self.assertIsNotNone(acc)
        self.assertEqual(acc.balance, 0.0)

    def test_deposit_operation(self):
        self.command_service.open_account(102)
        self.command_service.execute_operation(102, DepositOperation(500))
        self.assertEqual(self.repo.get(102).balance, 500)

    def test_withdraw_operation(self):
        self.command_service.open_account(103)
        self.command_service.execute_operation(103, DepositOperation(1000))
        self.command_service.execute_operation(103, WithdrawOperation(400))
        self.assertEqual(self.repo.get(103).balance, 600)

    def test_withdraw_insufficient_funds(self):
        self.command_service.open_account(104)
        with self.assertRaises(ValueError):
            self.command_service.execute_operation(104, WithdrawOperation(100))

    def test_generate_statement(self):
        self.command_service.open_account(105)
        self.command_service.execute_operation(105, DepositOperation(777))
        statement = self.statement_service.generate_statement(105)
        self.assertIn("777", statement)
        self.assertIn("105", statement)

if __name__ == "__main__":
    unittest.main()