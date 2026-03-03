"""Observer pattern for Application Logging."""
import logging
import os
import pandas as pd
from app.calculator_config import Config

class HistoryObserver:
    """Observer interface."""
    def update(self, action: str, df: pd.DataFrame): pass

class LoggingObserver(HistoryObserver):
    """Observer that logs calculations and actions to a file."""
    def __init__(self):
        os.makedirs(Config.LOG_DIR, exist_ok=True)
        logging.basicConfig(
            filename=Config.LOG_FILE,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding=Config.DEFAULT_ENCODING
        )
        self.logger = logging.getLogger(__name__)

    def update(self, action: str, df: pd.DataFrame):
        if action == "add" and not df.empty:
            latest = df.iloc[-1]
            self.logger.info(f"Operation: {latest['operation']} | Operands: {latest['a']}, {latest['b']} | Result: {latest['result']}")
        elif action in ["clear", "undo", "redo", "save", "load"]:
            self.logger.info(f"System Action executed: {action.upper()}")