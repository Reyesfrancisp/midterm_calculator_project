import pytest
from app.input_validators import validate_number
from app.exceptions import ValidationError
from app.calculator_config import Config


# Test valid numeric inputs that should successfully convert to floats
@pytest.mark.parametrize("value, expected", [
    ("5", 5.0), 
    ("-10.5", -10.5), 
    ("0", 0.0), 
    ("  42  ", 42.0),              # Leading/trailing whitespace
    ("1,000.50", 1000.5),          # Comma-separated number
    ("1e3", 1000.0),               # Scientific notation (positive)
    ("-2.5e-2", -0.025),           # Scientific notation (negative fractional)
    ("\n \t 99.9 \r", 99.9)        # Extreme whitespace characters
])
def test_validate_number_valid(value, expected):
    
    # validate_number should correctly parse and convert to float
    assert validate_number(value) == expected


# Test inputs that should be rejected as invalid numbers
@pytest.mark.parametrize("value", [
    "abc", "", "   ", "inf", "-inf", "nan", "1.2.3", "5a", "None"
])
def test_validate_number_invalid(value):
    
    # Invalid values should raise a ValidationError
    with pytest.raises(ValidationError):
        validate_number(value)


# Test behavior when numbers are at or beyond configured input limits
def test_validate_number_boundaries():
    
    original_limit = Config.MAX_INPUT_VALUE
    Config.MAX_INPUT_VALUE = 100.0  # Temporarily restrict allowed range
    
    # Values exactly at the boundary should be accepted
    assert validate_number("100") == 100.0
    assert validate_number("-100") == -100.0
    
    # Values just outside the boundary should raise an error
    with pytest.raises(ValidationError, match="Value exceeds maximum"):
        validate_number("100.0001")
        
    with pytest.raises(ValidationError, match="Value exceeds maximum"):
        validate_number("-100.0001")
        
    # Restore original configuration value
    Config.MAX_INPUT_VALUE = original_limit