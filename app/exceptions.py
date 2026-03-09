"""Custom exceptions for the calculator application."""


class CalculatorException(Exception):
    """Base exception for all calculator-related errors."""
    pass


class OperationError(CalculatorException):
    """Raised when an invalid or unsupported operation is requested."""
    pass


class ValidationError(CalculatorException):
    """Raised when user input fails validation checks."""
    pass


class DivisionByZeroError(OperationError):
    """Raised when attempting to divide a number by zero."""
    pass