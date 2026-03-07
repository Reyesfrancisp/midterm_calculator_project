import pytest
from app.exceptions import CalculatorException, OperationError, ValidationError, DivisionByZeroError


# Verify each custom exception can be raised and returns the correct message
@pytest.mark.parametrize("exception_class, message", [
    (CalculatorException, "Base error"),
    (OperationError, "Invalid operation"),
    (ValidationError, "Invalid input"),
    (DivisionByZeroError, "Cannot divide by zero")
])
def test_exceptions_raise(exception_class, message):

    # Ensure the exception is raised with the expected message
    with pytest.raises(exception_class, match=message):
        raise exception_class(message)


# Confirm the custom exception hierarchy is implemented correctly
def test_exception_inheritance():
    """Proves custom exceptions properly inherit from base classes."""

    # DivisionByZeroError should be a specialized OperationError
    assert issubclass(DivisionByZeroError, OperationError)

    # OperationError should inherit from the base calculator exception
    assert issubclass(OperationError, CalculatorException)

    # ValidationError should also inherit from the base calculator exception
    assert issubclass(ValidationError, CalculatorException)