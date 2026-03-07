import pytest
import pandas as pd
from unittest.mock import patch
from app.history import HistoryManager, AutoSaveObserver
from app.calculator_config import Config


# Fixture that provides a clean HistoryManager instance for each test
@pytest.fixture
def history_manager():
    hm = HistoryManager()
    hm.clear()  # Ensure history starts empty
    return hm


# Verify the history dataframe has the expected schema
def test_history_dataframe_structure(history_manager):
    """Ensures the dataframe contains exactly the required columns."""
    
    expected_columns = ['timestamp', 'operation', 'a', 'b', 'result']
    assert list(history_manager.df.columns) == expected_columns


# Ensure results are rounded according to the configured precision
def test_history_precision_rounding(history_manager):
    """Ensures results are rounded to the configured precision before saving."""
    
    original_precision = Config.PRECISION
    Config.PRECISION = 2  # Temporarily override precision
    
    history_manager.add_record('divide', 10, 3, 3.33333333)

    # Stored result should be rounded to 2 decimal places
    assert history_manager.df.iloc[-1]['result'] == 3.33
    
    # Restore original configuration value
    Config.PRECISION = original_precision


# Verify the history size does not exceed MAX_HISTORY_SIZE
def test_add_record_maintains_max_size(history_manager):
    
    original_max = Config.MAX_HISTORY_SIZE
    Config.MAX_HISTORY_SIZE = 2  # Limit history to 2 records
    
    history_manager.add_record('add', 1, 1, 2)
    history_manager.add_record('add', 2, 2, 4)
    history_manager.add_record('add', 3, 3, 6)  # Oldest record should be removed
    
    assert len(history_manager.df) == 2
    assert history_manager.df.iloc[-1]['result'] == 6
    assert history_manager.df.iloc[0]['result'] == 4
    
    Config.MAX_HISTORY_SIZE = original_max


# Verify the AutoSaveObserver triggers saving when a record is added
@patch('app.history.pd.DataFrame.to_csv')
def test_auto_save_observer(mock_to_csv, history_manager):

    Config.AUTO_SAVE = True

    # Attach autosave observer
    history_manager.add_observer(AutoSaveObserver())

    # Adding a record should trigger a CSV save
    history_manager.add_record('add', 1, 1, 2)

    mock_to_csv.assert_called_once()


# Test successful loading of history from a CSV file
@patch('app.history.pd.read_csv')
@patch('app.history.os.path.exists', return_value=True)
def test_load_history_success(_mock_exists, mock_read_csv, history_manager):

    # Simulate loading a valid dataframe from disk
    mock_read_csv.return_value = pd.DataFrame(
        columns=['timestamp', 'operation', 'a', 'b', 'result']
    )

    assert history_manager.load_history() is True


# Test displaying history output to the console
def test_display(history_manager, capsys):

    # When empty, the system should notify the user
    history_manager.display()
    assert "History is empty." in capsys.readouterr().out

    # Add a record and verify it appears in the display output
    history_manager.add_record('add', 1, 1, 2)
    history_manager.display()
    assert "add" in capsys.readouterr().out


# Ensure loading fails gracefully when the CSV file is empty
@patch('app.history.pd.read_csv', side_effect=pd.errors.EmptyDataError)
@patch('app.history.os.path.exists', return_value=True)
def test_load_history_empty_data_error(_mock_exists, _mock_read_csv, history_manager):

    assert history_manager.load_history() is False


# Ensure save_history handles filesystem errors safely
@patch('app.history.os.makedirs', side_effect=Exception("Disk Full Error"))
def test_save_history_exception_os(_mock_makedirs, history_manager):

    assert history_manager.save_history() is False


# Test the normal successful path of saving history
@patch('app.history.pd.DataFrame.to_csv')
def test_save_history_success_path(mock_to_csv):

    hm = HistoryManager()

    # Save should return True and attempt to write CSV
    assert hm.save_history() is True
    mock_to_csv.assert_called_once()


# Verify undo and redo functionality works correctly
def test_history_undo_redo(history_manager):
    """Covers successful undo and redo operations."""

    history_manager.add_record('add', 1, 1, 2)
    history_manager.add_record('add', 2, 2, 4)

    # Undo should revert to the previous state
    assert history_manager.undo() is True
    assert len(history_manager.df) == 1

    # Redo should restore the removed record
    assert history_manager.redo() is True
    assert len(history_manager.df) == 2