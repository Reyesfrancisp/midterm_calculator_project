"""Implements Strategy, Factory, and Command design patterns for calculator operations."""

from abc import ABC, abstractmethod
from app.operations import (
    add, subtract, multiply, divide, power, root,
    modulus, int_divide, percent, abs_diff
)
from app.exceptions import OperationError


# ==========================================
# STRATEGY PATTERN
# ==========================================

class CalculationStrategy:
    """Encapsulates a calculation algorithm (operation)."""

    def __init__(self, operation_func):
        # Store the function that performs the calculation
        self.operation_func = operation_func

    def execute(self, a: float, b: float) -> float:
        """Execute the stored operation."""
        return self.operation_func(a, b)


# ==========================================
# FACTORY PATTERN
# ==========================================

class OperationFactory:
    """Creates CalculationStrategy objects based on operation name."""

    # Maps operation names to their corresponding functions
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
        """Return a CalculationStrategy for the requested operation."""
        if operation_name not in cls._operations:
            raise OperationError(f"Unknown operation: {operation_name}")

        return CalculationStrategy(cls._operations[operation_name])


# ==========================================
# COMMAND PATTERN
# ==========================================

class Command(ABC):
    """Abstract base class for all commands."""

    @abstractmethod
    def execute(self) -> float:
        """Execute the command."""
        pass  # pragma: no cover


class CalculateCommand(Command):
    """Command that performs a calculation."""

    def __init__(self, op_name: str, a: float, b: float):
        # Store operation name and operands
        self.op_name = op_name
        self.a = a
        self.b = b

        # Use the factory to obtain the correct strategy
        self.strategy = OperationFactory.get_strategy(op_name)

    def execute(self) -> float:
        """Run the calculation using the selected strategy."""
        return self.strategy.execute(self.a, self.b)


class CommandInvoker:
    """Executes commands and keeps a history of executed commands."""

    def __init__(self):
        # Queue storing executed commands
        self._command_queue = []

    def execute_command(self, command: Command) -> float:
        """Execute a command and store it in the queue."""
        self._command_queue.append(command)
        return command.execute()

    def get_queue_size(self) -> int:
        """Return the number of commands executed."""
        return len(self._command_queue)

    def clear_queue(self):
        """Remove all commands from the queue."""
        self._command_queue.clear()