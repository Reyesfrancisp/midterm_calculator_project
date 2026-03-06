import pytest
from app.calculator_config import Config

def test_config_defaults_loaded():
    assert isinstance(Config.MAX_HISTORY_SIZE, int)
    assert isinstance(Config.PRECISION, int)
    assert isinstance(Config.MAX_INPUT_VALUE, float)
    assert isinstance(Config.AUTO_SAVE, bool)