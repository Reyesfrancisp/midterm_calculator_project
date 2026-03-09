"""Observer pattern for application logging."""

import logging
import os
import pandas as pd
from app.calculator_config import Config


class HistoryObserver:
    """Observer interface for reacting to history updates."""

    def update(self, action: str, df: pd.DataFrame):
        """Method called when the history state changes."""
        pass  # pragma: no cover


class LoggingObserver(HistoryObserver):
    """Observer that logs calculator operations and system actions."""

    def __init__(self):
        # Ensure the log directory exists
        os.makedirs(Config.LOG_DIR, exist_ok=True)

        # Configure the logging system
        logging.basicConfig(
            filename=Config.LOG_FILE,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding=Config.DEFAULT_ENCODING
        )

        # Create a logger instance for this module
        self.logger = logging.getLogger(__name__)

    def update(self, action: str, df: pd.DataFrame):
        """Log history updates based on the action performed."""

        # Log the most recent calculation when a new record is added
        if action == "add" and not df.empty:
            latest = df.iloc[-1]

            self.logger.info(
                f"Operation: {latest['operation']} | "
                f"Operands: {latest['a']}, {latest['b']} | "
                f"Result: {latest['result']}"
            )

        # Log system-level history actions
        elif action in ["clear", "undo", "redo", "save", "load"]:
            self.logger.info(f"System Action executed: {action.upper()}")