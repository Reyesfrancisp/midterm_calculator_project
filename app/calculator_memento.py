"""Memento pattern for Undo/Redo state management."""
import pandas as pd

class HistoryMemento:
    """Stores a snapshot of the pandas DataFrame."""
    def __init__(self, state: pd.DataFrame):
        self._state = state.copy(deep=True)

    def get_state(self) -> pd.DataFrame:
        return self._state.copy(deep=True)

class HistoryCaretaker:
    """Manages mementos to handle undo and redo operations."""
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def save_state(self, state: pd.DataFrame):
        self._undo_stack.append(HistoryMemento(state))
        self._redo_stack.clear() 

    def undo(self, current_state: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
        if not self._undo_stack:
            return current_state, False
        self._redo_stack.append(HistoryMemento(current_state))
        return self._undo_stack.pop().get_state(), True

    def redo(self, current_state: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
        if not self._redo_stack:
            return current_state, False
        self._undo_stack.append(HistoryMemento(current_state))
        return self._redo_stack.pop().get_state(), True