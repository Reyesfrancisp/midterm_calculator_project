import pytest
from app.calculation import OperationFactory, CalculationStrategy, CalculateCommand, CommandInvoker
from app.exceptions import OperationError

# Test multiple valid operations using parameterized inputs
# Ensures the factory returns the correct strategy and calculation result
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
    # Retrieve the calculation strategy from the factory
    strategy = OperationFactory.get_strategy(op_name)

    # Verify the returned object follows the Strategy interface
    assert isinstance(strategy, CalculationStrategy)

    # Verify the operation produces the expected result
    assert strategy.execute(a, b) == expected


# Ensure invalid operation names raise the proper exception
@pytest.mark.parametrize("invalid_op", ["unknown", "", "ADD"])
def test_operation_factory_invalid(invalid_op):
    with pytest.raises(OperationError):
        OperationFactory.get_strategy(invalid_op)


def test_calculate_command_state():
    """Verify that the command stores inputs correctly and executes the operation."""
    
    # Create command with operation and operands
    cmd = CalculateCommand('add', 5, 5)

    # Confirm initialization values are stored properly
    assert cmd.op_name == 'add'
    assert cmd.a == 5
    assert cmd.b == 5

    # Ensure execution performs the correct calculation
    assert cmd.execute() == 10.0


def test_command_invoker_queuing():
    """Test that the invoker executes commands and tracks them in its queue."""
    
    invoker = CommandInvoker()

    # Create two calculation commands
    cmd1 = CalculateCommand('add', 1, 2)
    cmd2 = CalculateCommand('multiply', 3, 4)

    # Execute commands and verify results
    assert invoker.execute_command(cmd1) == 3.0
    assert invoker.execute_command(cmd2) == 12.0

    # Queue should contain the executed commands
    assert invoker.get_queue_size() == 2

    # Clearing the queue should remove all commands
    invoker.clear_queue()
    assert invoker.get_queue_size() == 0


# Ensure invalid operations passed to the command raise an error
def test_calculate_command_invalid_operation():
    with pytest.raises(OperationError):
        CalculateCommand('invalid_op', 1, 1)