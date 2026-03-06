import pytest
from app.calculation import OperationFactory, CalculationStrategy
from app.exceptions import OperationError

@pytest.mark.parametrize("op_name, a, b, expected", [
    ('add', 5.5, 4.5, 10.0),
    ('subtract', 10, 4.5, 5.5),
    ('multiply', -2, 3, -6.0),
    ('divide', 10, 4, 2.5),
    ('power', 2, 3, 8.0),
    ('root', 27, 3, 3.0),
    ('modulus', 10, 3, 1.0),
    ('int_divide', 10, 3, 3.0),
    ('percent', 1, 4, 25.0),
    ('abs_diff', 2, 10, 8.0)
])
def test_operation_factory_valid(op_name, a, b, expected):
    strategy = OperationFactory.get_strategy(op_name)
    assert isinstance(strategy, CalculationStrategy)
    assert strategy.execute(a, b) == expected

@pytest.mark.parametrize("invalid_op", ["unknown", "", "ADD"])
def test_operation_factory_invalid(invalid_op):
    with pytest.raises(OperationError):
        OperationFactory.get_strategy(invalid_op)