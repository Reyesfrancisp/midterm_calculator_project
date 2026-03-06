import pytest
import pandas as pd
from unittest.mock import patch
from app.history import HistoryManager, AutoSaveObserver
from app.calculator_config import Config

@pytest.fixture
def history_manager():
    hm = HistoryManager()
    hm.clear()
    return hm

def test_add_record_maintains_max_size(history_manager):
    original_max = Config.MAX_HISTORY_SIZE
    Config.MAX_HISTORY_SIZE = 2
    
    history_manager.add_record('add', 1, 1, 2)
    history_manager.add_record('add', 2, 2, 4)
    history_manager.add_record('add', 3, 3, 6)
    
    assert len(history_manager.df) == 2
    assert history_manager.df.iloc[-1]['result'] == 6
    assert history_manager.df.iloc[0]['result'] == 4
    Config.MAX_HISTORY_SIZE = original_max

@patch('app.history.pd.DataFrame.to_csv')
def test_auto_save_observer(mock_to_csv, history_manager):
    Config.AUTO_SAVE = True
    history_manager.add_observer(AutoSaveObserver())
    history_manager.add_record('add', 1, 1, 2)
    mock_to_csv.assert_called_once()

@patch('app.history.pd.read_csv')
@patch('app.history.os.path.exists', return_value=True)
def test_load_history_success(mock_exists, mock_read_csv, history_manager):
    mock_read_csv.return_value = pd.DataFrame({'timestamp': [], 'operation': [], 'a': [], 'b': [], 'result': []})
    assert history_manager.load_history() is True

def test_undo_redo(history_manager):
    history_manager.add_record('add', 1, 1, 2)
    history_manager.add_record('add', 2, 2, 4)
    assert history_manager.undo() is True
    assert len(history_manager.df) == 1
    assert history_manager.redo() is True
    assert len(history_manager.df) == 2

def test_display(history_manager, capsys):
    history_manager.display()
    assert "History is empty." in capsys.readouterr().out
    history_manager.add_record('add', 1, 1, 2)
    history_manager.display()
    assert "add" in capsys.readouterr().out