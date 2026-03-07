import pytest
from unittest.mock import patch
from app.calculator import CalculatorFacade, repl


# Test the CalculatorFacade calculation flow with various valid and invalid inputs
@pytest.mark.parametrize("op, a, b, expected_out", [
    ('add', '1.5', '1.5', 'Result: 3\n'),
    ('modulus', '10', '3', 'Result: 1\n'),
    ('divide', '10', '0', 'Error: Cannot divide by zero'),
    ('add', 'a', '5', 'Error: Invalid numeric input')
])
def test_facade_calculate(op, a, b, expected_out, capsys):
    facade = CalculatorFacade()

    # Perform the calculation through the facade
    facade.calculate(op, a, b)

    # Capture console output and verify expected message
    assert expected_out in capsys.readouterr().out


# Ensure unexpected internal errors are caught and displayed
@patch('app.calculation.OperationFactory.get_strategy', side_effect=Exception("Generic Boom"))
def test_facade_calculate_unexpected_error(_mock_strategy, capsys):
    facade = CalculatorFacade()
    facade.calculate('add', '5', '5')

    # The facade should catch the exception and print an error message
    assert "Unexpected Error: Generic Boom" in capsys.readouterr().out


# Test REPL command parsing and behavior with different user inputs
@pytest.mark.parametrize("inputs, expected_out", [
    (['add 5 5', 'exit'], 'Result: 10'),
    (['add    5    10', 'exit'], 'Result: 15'),  # Handles excessive spacing
    (['percent', '1', '4', 'exit'], 'Result: 25'),
    (['help', 'exit'], 'HELP MENU'),
    (['bad_command', 'exit'], 'Unknown command'),
    (['', 'exit'], 'Goodbye!')  # Empty input before exiting
])
@patch('app.history.os.path.exists', return_value=False)
def test_repl_commands(_mock_exists, inputs, expected_out, capsys):

    # Mock user input sequence for the REPL
    with patch('builtins.input', side_effect=inputs):
        repl()

        # Verify the expected output appeared
        assert expected_out in capsys.readouterr().out


# Ensure the REPL exits cleanly if an EOF signal occurs
@patch('builtins.input', side_effect=EOFError)
def test_repl_eof(_mock_input):
    repl()  # Should terminate without raising an exception


# Test failure paths for REPL history-related commands
@patch('app.history.HistoryManager.save_history', return_value=False)
@patch('app.history.HistoryManager.undo', return_value=False)
@patch('app.history.HistoryManager.redo', return_value=False)
@patch('app.history.HistoryManager.load_history', return_value=False)
def test_repl_command_failures(_mock_load, _mock_redo, _mock_undo, _mock_save, capsys):

    # Provide commands that trigger failure responses
    inputs = ['undo', 'redo', 'save', 'load', 'add 5', 'exit']

    with patch('builtins.input', side_effect=inputs):
        repl()

        out = capsys.readouterr().out

        # Verify correct error messages for each failed operation
        assert "Cannot undo" in out
        assert "Cannot redo" in out
        assert "Error saving history" in out
        assert "No existing history found" in out
        assert "Usage: <operation> <x> <y>" in out


# Test successful paths for history-related REPL commands
@patch('app.history.HistoryManager.undo', return_value=True)
@patch('app.history.HistoryManager.redo', return_value=True)
@patch('app.history.HistoryManager.load_history', return_value=True)
def test_repl_command_success_paths(_mock_load, _mock_redo, _mock_undo, capsys):

    inputs = ['undo', 'redo', 'load', 'exit']

    with patch('builtins.input', side_effect=inputs):
        repl()

        out = capsys.readouterr().out

        # Verify success messages appear
        assert "Reverted to previous state" in out
        assert "Restored state" in out
        assert "History manually loaded" in out


# Test interactive math mode where the REPL asks for operands separately
def test_repl_interactive_math(capsys):

    inputs = ['add', '5', '10', 'exit']

    with patch('builtins.input', side_effect=inputs):
        repl()

        out = capsys.readouterr().out

        # Confirm correct calculation result
        assert "Result: 15" in out


# Test history display, clearing, and manual saving commands
@patch('app.history.os.path.exists', return_value=False)
@patch('app.history.HistoryManager.save_history', return_value=True)
def test_repl_history_clear_save(_mock_save, _mock_exists, capsys):

    inputs = ['history', 'clear', 'save', 'exit']

    with patch('builtins.input', side_effect=inputs):
        repl()

        out = capsys.readouterr().out

        # Verify correct responses for history operations
        assert "History is empty." in out
        assert "History cleared." in out
        assert "History manually saved" in out