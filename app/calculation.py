"""Strategy and Factory design patterns for calculations."""
from app.operations import (add, subtract, multiply, divide, power, root, 
                            modulus, int_divide, percent, abs_diff)
from app.exceptions import OperationError

class CalculationStrategy:
    """Strategy context for executing operations."""
    def __init__(self, operation_func):
        self.operation_func = operation_func

    def execute(self, a: float, b: float) -> float:
        return self.operation_func(a, b)

class OperationFactory:
    """Factory to instantiate strategies."""
    _operations = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        'power': power,
        'root': root,
        'modulus': modulus,
        'int_divide': int_divide,
        'percent': percent,
        'abs_diff': abs_diff
    }

    @classmethod
    def get_strategy(cls, operation_name: str) -> CalculationStrategy:
        if operation_name not in cls._operations:
            raise OperationError(f"Unknown operation: {operation_name}")
        return CalculationStrategy(cls._operations[operation_name])