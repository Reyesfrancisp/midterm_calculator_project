"""Memento pattern for Undo/Redo state management."""

import pandas as pd


class HistoryMemento:
    """Stores a snapshot of the calculation history DataFrame."""

    def __init__(self, state: pd.DataFrame):
        # Save a deep copy so the stored state cannot be modified externally
        self._state = state.copy(deep=True)

    def get_state(self) -> pd.DataFrame:
        """Return a copy of the stored state."""
        return self._state.copy(deep=True)


class HistoryCaretaker:
    """Manages saved states to support undo and redo operations."""

    def __init__(self):
        # Stack of previous states for undo operations
        self._undo_stack = []

        # Stack of states that can be restored with redo
        self._redo_stack = []

    def save_state(self, state: pd.DataFrame):
        """Save the current state before a change occurs."""
        self._undo_stack.append(HistoryMemento(state))

        # Any new action invalidates the redo history
        self._redo_stack.clear()

    def undo(self, current_state: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
        """Restore the most recent previous state."""
        if not self._undo_stack:
            return current_state, False  # No state available to undo

        # Save current state to allow redo later
        self._redo_stack.append(HistoryMemento(current_state))

        return self._undo_stack.pop().get_state(), True

    def redo(self, current_state: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
        """Reapply the most recently undone state."""
        if not self._redo_stack:
            return current_state, False  # No state available to redo

        # Save current state back to the undo stack
        self._undo_stack.append(HistoryMemento(current_state))

        return self._redo_stack.pop().get_state(), True