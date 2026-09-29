from interfaces.protocols import ICalculationStrategy

class InterestStrategy(ICalculationStrategy):
    """Расчет процентов (10%)"""
    def calculate(self, amount: float) -> float:
        return amount * 0.10

class CommissionStrategy(ICalculationStrategy):
    """Обычная комиссия (5%)"""
    def calculate(self, amount: float) -> float:
        return amount * 0.05

class PreferentialStrategy(ICalculationStrategy):
    """Льготный расчет (1%)"""
    def calculate(self, amount: float) -> float:
        return amount * 0.01