import pytest
import pandas as pd
from unittest.mock import patch
from app.logger import LoggingObserver


# Verify that the LoggingObserver logs a message when an operation is added
@patch('app.logger.logging.Logger.info')
def test_logging_observer_add(mock_info):
    
    observer = LoggingObserver()

    # Simulate a dataframe containing a single calculation record
    df = pd.DataFrame(
        [['2026-01-01T12:00:00', 'add', 5, 5, 10]],
        columns=['timestamp', 'operation', 'a', 'b', 'result']
    )

    # Trigger observer update for an add operation
    observer.update('add', df)

    # Ensure a log entry was created
    mock_info.assert_called_once()

    # Verify the log message includes the operation name
    assert "Operation: add" in mock_info.call_args[0][0]


# Verify that system actions (clear, undo, redo, save, load) are logged
@patch('app.logger.logging.Logger.info')
@pytest.mark.parametrize("action", ["clear", "undo", "redo", "save", "load"])
def test_logging_observer_system_actions(mock_info, action):

    observer = LoggingObserver()

    # System actions do not require a populated dataframe
    df = pd.DataFrame()

    # Trigger observer update for a system-level action
    observer.update(action, df)

    # Ensure the logger was called once
    mock_info.assert_called_once()

    # Confirm the log message includes the action name
    assert action.upper() in mock_info.call_args[0][0]