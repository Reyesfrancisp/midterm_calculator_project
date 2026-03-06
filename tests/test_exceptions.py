import pytest
from app.exceptions import CalculatorException, OperationError, ValidationError, DivisionByZeroError

@pytest.mark.parametrize("exception_class, message", [
    (CalculatorException, "Base error"),
    (OperationError, "Invalid operation"),
    (ValidationError, "Invalid input"),
    (DivisionByZeroError, "Cannot divide by zero")
])
def test_exceptions_raise(exception_class, message):
    with pytest.raises(exception_class, match=message):
        raise exception_class(message)