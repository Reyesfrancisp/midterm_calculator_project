"""Pandas history management and Auto-Save Observer."""
import os
import pandas as pd
from datetime import datetime
from app.calculator_config import Config
from app.calculator_memento import HistoryCaretaker
from app.logger import HistoryObserver

class AutoSaveObserver(HistoryObserver):
    """Observer that auto-saves the dataframe to a CSV on changes if configured."""
    def update(self, action: str, df: pd.DataFrame):
        if Config.AUTO_SAVE and action in ["add", "clear", "undo", "redo"]:
            os.makedirs(Config.HISTORY_DIR, exist_ok=True)
            df.to_csv(Config.HISTORY_FILE, index=False)

class HistoryManager:
    """Manages history utilizing pandas DataFrames."""
    def __init__(self):
        self.columns = ['timestamp', 'operation', 'a', 'b', 'result']
        self.df = pd.DataFrame(columns=self.columns)
        self.observers = []
        self.caretaker = HistoryCaretaker()
        self.load_history()

    def add_observer(self, observer: HistoryObserver):
        self.observers.append(observer)

    def notify_observers(self, action: str):
        for obs in self.observers:
            obs.update(action, self.df)

    def load_history(self) -> bool:
        if os.path.exists(Config.HISTORY_FILE):
            try:
                self.df = pd.read_csv(Config.HISTORY_FILE)
                self.caretaker.save_state(self.df)
                self.notify_observers("load")
                return True
            except pd.errors.EmptyDataError:
                self.df = pd.DataFrame(columns=self.columns)
        return False

    def save_history(self) -> bool:
        try:
            os.makedirs(Config.HISTORY_DIR, exist_ok=True)
            self.df.to_csv(Config.HISTORY_FILE, index=False)
            self.notify_observers("save")
            return True
        except Exception:
            return False

    def add_record(self, operation: str, a: float, b: float, result: float):
        self.caretaker.save_state(self.df)
        
        # Apply precision setting
        result = round(result, Config.PRECISION)
        timestamp = datetime.now().isoformat()
        
        new_row = pd.DataFrame([[timestamp, operation, a, b, result]], columns=self.columns)
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        
        # Enforce Max History Size
        if len(self.df) > Config.MAX_HISTORY_SIZE:
            self.df = self.df.tail(Config.MAX_HISTORY_SIZE).reset_index(drop=True)
            
        self.notify_observers("add")

    def clear(self):
        self.caretaker.save_state(self.df)
        self.df = pd.DataFrame(columns=self.columns)
        self.notify_observers("clear")

    def undo(self) -> bool:
        self.df, success = self.caretaker.undo(self.df)
        if success: self.notify_observers("undo")
        return success

    def redo(self) -> bool:
        self.df, success = self.caretaker.redo(self.df)
        if success: self.notify_observers("redo")
        return success

    def display(self):
        if self.df.empty:
            print("  History is empty.")
        else:
            print("\n", self.df.to_string(index=True), "\n")