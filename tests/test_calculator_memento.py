import pandas as pd
from app.calculator_memento import HistoryMemento, HistoryCaretaker

def test_memento_state_protection():
    df = pd.DataFrame({'a': [1]})
    memento = HistoryMemento(df)
    df.loc[0, 'a'] = 99
    assert memento.get_state().iloc[0]['a'] == 1

def test_caretaker_undo_redo():
    caretaker = HistoryCaretaker()
    df1 = pd.DataFrame({'val': [1]})
    df2 = pd.DataFrame({'val': [1, 2]})
    
    caretaker.save_state(df1)
    restored_df, success = caretaker.undo(df2)
    assert success is True
    assert restored_df.equals(df1)
    
    redone_df, success = caretaker.redo(restored_df)
    assert success is True
    assert redone_df.equals(df2)

@pytest.mark.parametrize("empty_data", [{'val': []}])
def test_caretaker_empty_stacks(empty_data):
    caretaker = HistoryCaretaker()
    df = pd.DataFrame(empty_data)
    
    _, success = caretaker.undo(df)
    assert success is False
    
    _, success = caretaker.redo(df)
    assert success is False