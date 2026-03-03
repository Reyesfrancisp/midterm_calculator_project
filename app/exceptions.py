"""Custom exceptions for the calculator application."""

class CalculatorException(Exception):
    """Base class for all calculator exceptions."""
    pass

class OperationError(CalculatorException):
    pass

class ValidationError(CalculatorException):
    pass

class DivisionByZeroError(OperationError):
    pass