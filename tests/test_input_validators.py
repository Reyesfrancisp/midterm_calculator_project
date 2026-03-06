import pytest
from app.input_validators import validate_number
from app.exceptions import ValidationError
from app.calculator_config import Config

@pytest.mark.parametrize("value, expected", [
    ("5", 5.0), ("-10.5", -10.5), ("0", 0.0), ("  42  ", 42.0), ("1,000.50", 1000.5)
])
def test_validate_number_valid(value, expected):
    assert validate_number(value) == expected

@pytest.mark.parametrize("value", [
    "abc", "", "inf", "-inf", "nan", "1.2.3"
])
def test_validate_number_invalid(value):
    with pytest.raises(ValidationError):
        validate_number(value)

def test_validate_number_max_limit():
    original_limit = Config.MAX_INPUT_VALUE
    Config.MAX_INPUT_VALUE = 100.0
    with pytest.raises(ValidationError, match="Value exceeds maximum"):
        validate_number("101")
    Config.MAX_INPUT_VALUE = original_limit