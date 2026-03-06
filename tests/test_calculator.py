import pytest
from unittest.mock import patch
from app.calculator import CalculatorFacade, repl

@pytest.mark.parametrize("op, a, b, expected_out", [
    ('add', '1.5', '1.5', 'Result: 3\n'),
    ('modulus', '10', '3', 'Result: 1\n'),
    ('divide', '10', '0', 'Error: Cannot divide by zero'),
    ('add', 'a', '5', 'Error: Invalid numeric input')
])
def test_facade_calculate(op, a, b, expected_out, capsys):
    facade = CalculatorFacade()
    facade.calculate(op, a, b)
    assert expected_out in capsys.readouterr().out

@patch('app.calculation.OperationFactory.get_strategy', side_effect=Exception("Generic Boom"))
def test_facade_calculate_unexpected_error(mock_strategy, capsys):
    facade = CalculatorFacade()
    facade.calculate('add', '5', '5')
    assert "Unexpected Error: Generic Boom" in capsys.readouterr().out

@pytest.mark.parametrize("inputs, expected_out", [
    (['add 5 5', 'exit'], 'Result: 10'),
    (['percent', '1', '4', 'exit'], 'Result: 25'),
    (['help', 'exit'], 'HELP MENU'),
    (['bad_command', 'exit'], 'Unknown command'),
    (['', 'exit'], 'Goodbye!')
])
@patch('app.history.os.path.exists', return_value=False)
def test_repl_commands(mock_exists, inputs, expected_out, capsys):
    with patch('builtins.input', side_effect=inputs):
        repl()
        assert expected_out in capsys.readouterr().out

@patch('builtins.input', side_effect=EOFError)
def test_repl_eof(mock_input):
    repl()

@pytest.mark.parametrize("command_chain, expected_out", [
    (['history', 'exit'], 'History is empty.'),
    (['clear', 'exit'], 'History cleared.'),
    (['undo', 'exit'], 'Cannot undo.'),
    (['redo', 'exit'], 'Cannot redo.'),
    (['save', 'exit'], 'History manually saved'),
    (['load', 'exit'], 'No existing history found')
])
@patch('app.history.os.path.exists', return_value=False)
@patch('app.history.HistoryManager.save_history', return_value=True)
def test_repl_data_commands(mock_save, mock_exists, command_chain, expected_out, capsys):
    with patch('builtins.input', side_effect=command_chain):
        repl()
        assert expected_out in capsys.readouterr().out

@patch('app.history.HistoryManager.save_history', return_value=False)
@patch('app.history.HistoryManager.undo', return_value=False)
@patch('app.history.HistoryManager.redo', return_value=False)
@patch('app.history.HistoryManager.load_history', return_value=False)
def test_repl_command_failures(mock_load, mock_redo, mock_undo, mock_save, capsys):
    """Simulates failures to cover the else branches and the usage warning (line 115)."""
    inputs = ['undo', 'redo', 'save', 'load', 'add 5', 'exit']
    with patch('builtins.input', side_effect=inputs):
        repl()
        out = capsys.readouterr().out
        assert "Cannot undo" in out
        assert "Cannot redo" in out
        assert "Error saving history" in out
        assert "No existing history found" in out
        assert "Usage: <operation> <x> <y>" in out

@patch('app.history.HistoryManager.undo', return_value=True)
@patch('app.history.HistoryManager.redo', return_value=True)
@patch('app.history.HistoryManager.load_history', return_value=True)
def test_repl_command_success_paths(mock_load, mock_redo, mock_undo, capsys):
    """Forces undo, redo, and load to succeed to cover their 'if' blocks."""
    inputs = ['undo', 'redo', 'load', 'exit']
    with patch('builtins.input', side_effect=inputs):
        repl()
        out = capsys.readouterr().out
        assert "Reverted to previous state" in out
        assert "Restored state" in out
        assert "History manually loaded" in out