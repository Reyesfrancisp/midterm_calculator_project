import pytest
from app.calculation import OperationFactory, CalculationStrategy, CalculateCommand, CommandInvoker
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

def test_calculate_command_execution():
    cmd = CalculateCommand('add', 5, 5)
    assert cmd.execute() == 10.0

def test_command_invoker_queuing():
    invoker = CommandInvoker()
    cmd1 = CalculateCommand('add', 1, 2)
    cmd2 = CalculateCommand('multiply', 3, 4)
    
    assert invoker.execute_command(cmd1) == 3.0
    assert invoker.execute_command(cmd2) == 12.0
    
    assert invoker.get_queue_size() == 2
    
    invoker.clear_queue()
    assert invoker.get_queue_size() == 0

def test_calculate_command_invalid_operation():
    with pytest.raises(OperationError):
        CalculateCommand('invalid_op', 1, 1)        