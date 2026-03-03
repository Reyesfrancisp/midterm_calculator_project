"""Input validation utilities."""
import math
from app.exceptions import ValidationError
from app.calculator_config import Config

def validate_number(value_str: str) -> float:
    """Validates and converts a string to a float using LBYL and EAFP paradigms."""
    clean_val = str(value_str).strip().replace(',', '')
    if not clean_val:
        raise ValidationError("Input cannot be empty.")

    try:
        parsed_float = float(clean_val)
    except ValueError:
        raise ValidationError(f"Invalid numeric input: '{value_str}'")

    if math.isnan(parsed_float) or math.isinf(parsed_float):
        raise ValidationError(f"Disallowed value: '{value_str}' (Infinity/NaN not supported).")
        
    if abs(parsed_float) > Config.MAX_INPUT_VALUE:
        raise ValidationError(f"Value exceeds maximum allowed limit of {Config.MAX_INPUT_VALUE}")

    return parsed_float