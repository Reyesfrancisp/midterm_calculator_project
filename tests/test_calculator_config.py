import pytest
from app.calculator_config import Config

# Verify that configuration values are loaded and have the correct data types
def test_config_defaults_loaded():
    
    # Maximum history size should be an integer
    assert isinstance(Config.MAX_HISTORY_SIZE, int)

    # Precision used for calculations should be an integer
    assert isinstance(Config.PRECISION, int)

    # Maximum allowed input value should be a float
    assert isinstance(Config.MAX_INPUT_VALUE, float)

    # Auto-save flag should be a boolean
    assert isinstance(Config.AUTO_SAVE, bool)