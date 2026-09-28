from repositories.memory_repository import MemoryAccountRepository
from services.bank_service import BankCommandService, StatementService
from ui.console import ConsoleUI

def main():
    repository = MemoryAccountRepository()
    
    command_service = BankCommandService(writer=repository, reader=repository)
    statement_service = StatementService(reader=repository)
    
    ui = ConsoleUI(command_service, statement_service)
    ui.run()

if __name__ == "__main__":
    main()