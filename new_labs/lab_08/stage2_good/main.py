from repositories.memory_repository import MemoryRepository
from ui.console import ConsoleUI

def main():
    repo = MemoryRepository()
    ui = ConsoleUI(repo)
    ui.run()

if __name__ == "__main__":
    main()