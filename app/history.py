"""Pandas history management and Auto-Save Observer."""

import os
import pandas as pd
from datetime import datetime
from app.calculator_config import Config
from app.calculator_memento import HistoryCaretaker
from app.logger import HistoryObserver


class AutoSaveObserver(HistoryObserver):
    """Observer that automatically saves history to CSV when changes occur."""

    def update(self, action: str, df: pd.DataFrame):
        # Auto-save history when enabled and relevant actions occur
        if Config.AUTO_SAVE and action in ["add", "clear", "undo", "redo"]:
            os.makedirs(Config.HISTORY_DIR, exist_ok=True)
            df.to_csv(Config.HISTORY_FILE, index=False)


class HistoryManager:
    """Manages calculation history using a pandas DataFrame."""

    def __init__(self):
        # Define the structure of the history table
        self.columns = ['timestamp', 'operation', 'a', 'b', 'result']

        # Initialize an empty DataFrame for storing history
        self.df = pd.DataFrame(columns=self.columns)

        # List of observers that react to history changes
        self.observers = []

        # Caretaker managing undo/redo state history (Memento Pattern)
        self.caretaker = HistoryCaretaker()

        # Load existing history from file if available
        self.load_history()

    def add_observer(self, observer: HistoryObserver):
        """Register an observer to receive history updates."""
        self.observers.append(observer)

    def notify_observers(self, action: str):
        """Notify all observers when history changes."""
        for obs in self.observers:
            obs.update(action, self.df)

    def load_history(self) -> bool:
        """Load calculation history from the configured CSV file."""
        if os.path.exists(Config.HISTORY_FILE):
            try:
                self.df = pd.read_csv(Config.HISTORY_FILE)

                # Save initial state for undo functionality
                self.caretaker.save_state(self.df)

                # Notify observers that history was loaded
                self.notify_observers("load")
                return True

            except pd.errors.EmptyDataError:
                # Handle case where CSV exists but is empty
                self.df = pd.DataFrame(columns=self.columns)

        return False

    def save_history(self) -> bool:
        """Manually save the current history to a CSV file."""
        try:
            os.makedirs(Config.HISTORY_DIR, exist_ok=True)
            self.df.to_csv(Config.HISTORY_FILE, index=False)

            # Notify observers that a save occurred
            self.notify_observers("save")
            return True

        except Exception:
            return False

    def add_record(self, operation: str, a: float, b: float, result: float):
        """Add a new calculation record to the history."""

        # Save current state before modifying history (for undo)
        self.caretaker.save_state(self.df)

        # Apply configured numeric precision to result
        result = round(result, Config.PRECISION)

        # Generate timestamp for the record
        timestamp = datetime.now().isoformat()

        # Create new history row
        new_row = pd.DataFrame([[timestamp, operation, a, b, result]], columns=self.columns)

        # Append the new record to the DataFrame
        self.df = pd.concat([self.df, new_row], ignore_index=True)

        # Enforce maximum history size limit
        if len(self.df) > Config.MAX_HISTORY_SIZE:
            self.df = self.df.tail(Config.MAX_HISTORY_SIZE).reset_index(drop=True)

        # Notify observers that a new record was added
        self.notify_observers("add")

    def clear(self):
        """Clear all stored calculation history."""

        # Save state before clearing (supports undo)
        self.caretaker.save_state(self.df)

        self.df = pd.DataFrame(columns=self.columns)

        # Notify observers of the clear action
        self.notify_observers("clear")

    def undo(self) -> bool:
        """Revert history to the previous state."""
        self.df, success = self.caretaker.undo(self.df)

        if success:
            self.notify_observers("undo")

        return success

    def redo(self) -> bool:
        """Restore the most recently undone history state."""
        self.df, success = self.caretaker.redo(self.df)

        if success:
            self.notify_observers("redo")

        return success

    def display(self):
        """Print the calculation history to the console."""
        if self.df.empty:
            print("  History is empty.")
        else:
            print("\n", self.df.to_string(index=True), "\n")