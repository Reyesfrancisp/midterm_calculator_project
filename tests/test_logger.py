import pytest
import pandas as pd
from unittest.mock import patch
from app.logger import LoggingObserver

@patch('app.logger.logging.Logger.info')
def test_logging_observer_add(mock_info):
    observer = LoggingObserver()
    df = pd.DataFrame([['2026-01-01T12:00:00', 'add', 5, 5, 10]], columns=['timestamp', 'operation', 'a', 'b', 'result'])
    observer.update('add', df)
    mock_info.assert_called_once()
    assert "Operation: add" in mock_info.call_args[0][0]

@patch('app.logger.logging.Logger.info')
@pytest.mark.parametrize("action", ["clear", "undo", "redo", "save", "load"])
def test_logging_observer_system_actions(mock_info, action):
    observer = LoggingObserver()
    df = pd.DataFrame()
    observer.update(action, df)
    mock_info.assert_called_once()
    assert action.upper() in mock_info.call_args[0][0]