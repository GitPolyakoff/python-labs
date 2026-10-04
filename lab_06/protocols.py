from typing import Protocol

# протокол. client и account соответствуют ему, потому что имеют этот метод
class Reportable(Protocol):
    def get_report_data(self) -> str:
        ...