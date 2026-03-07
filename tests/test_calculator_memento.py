import pytest
import pandas as pd
from app.calculator_memento import HistoryMemento, HistoryCaretaker


def test_memento_state_protection():
    """Ensure the saved memento keeps an independent copy of the dataframe."""
    
    # Create initial dataframe and store it in a memento
    df = pd.DataFrame({'a': [1]})
    memento = HistoryMemento(df)

    # Modify the original dataframe after saving the state
    df.loc[0, 'a'] = 99

    # The stored state should remain unchanged
    assert memento.get_state().iloc[0]['a'] == 1


def test_caretaker_complex_chain():
    """Test multiple undo and redo operations across saved states."""
    
    caretaker = HistoryCaretaker()

    # Create three different dataframe states
    df1 = pd.DataFrame({'val': [1]})
    df2 = pd.DataFrame({'val': [1, 2]})
    df3 = pd.DataFrame({'val': [1, 2, 3]})

    # Save the first two states
    caretaker.save_state(df1)
    caretaker.save_state(df2)

    # Current state is df3; undo should restore df2
    restored_2, success = caretaker.undo(df3)
    assert success is True
    assert restored_2.equals(df2)

    # Undo again should restore df1
    restored_1, success = caretaker.undo(restored_2)
    assert success is True
    assert restored_1.equals(df1)

    # Redo should move forward to df2 again
    redone_2, success = caretaker.redo(restored_1)
    assert success is True
    assert redone_2.equals(df2)


# Test behavior when undo/redo stacks are empty
@pytest.mark.parametrize("empty_data", [{'val': []}])
def test_caretaker_empty_stacks(empty_data):
    
    caretaker = HistoryCaretaker()

    # Create an empty dataframe state
    df = pd.DataFrame(empty_data)

    # Undo should fail because no previous state exists
    _, success = caretaker.undo(df)
    assert success is False

    # Redo should also fail because no future state exists
    _, success = caretaker.redo(df)
    assert success is False