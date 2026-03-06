"""Strategy, Factory, and Command design patterns for calculations."""
from abc import ABC, abstractmethod
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
        'add': add, 'subtract': subtract, 'multiply': multiply, 'divide': divide,
        'power': power, 'root': root, 'modulus': modulus, 'int_divide': int_divide,
        'percent': percent, 'abs_diff': abs_diff
    }

    @classmethod
    def get_strategy(cls, operation_name: str) -> CalculationStrategy:
        if operation_name not in cls._operations:
            raise OperationError(f"Unknown operation: {operation_name}")
        return CalculationStrategy(cls._operations[operation_name])

# ==========================================
# COMMAND PATTERN IMPLEMENTATION
# ==========================================

class Command(ABC):
    """Abstract Command interface."""
    @abstractmethod
    def execute(self) -> float:
        pass

class CalculateCommand(Command):
    """Concrete command to perform a calculation. Encapsulates the request."""
    def __init__(self, op_name: str, a: float, b: float):
        self.op_name = op_name
        self.a = a
        self.b = b
        # Automatically resolves the correct strategy using the Factory
        self.strategy = OperationFactory.get_strategy(op_name)

    def execute(self) -> float:
        return self.strategy.execute(self.a, self.b)

class CommandInvoker:
    """Invoker that executes commands and maintains a queue/history of requests."""
    def __init__(self):
        self._command_queue = []

    def execute_command(self, command: Command) -> float:
        self._command_queue.append(command)
        return command.execute()
        
    def get_queue_size(self) -> int:
        return len(self._command_queue)
    
    def clear_queue(self):
        self._command_queue.clear()