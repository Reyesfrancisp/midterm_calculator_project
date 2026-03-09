"""Input validation utilities."""

import math
from app.exceptions import ValidationError
from app.calculator_config import Config


def validate_number(value_str: str) -> float:
    """Validate and convert user input into a safe floating-point number."""

    # Normalize input by removing whitespace and thousands separators
    clean_val = str(value_str).strip().replace(',', '')

    # Ensure input is not empty
    if not clean_val:
        raise ValidationError("Input cannot be empty.")

    try:
        # Attempt to convert the cleaned string to a float (EAFP approach)
        parsed_float = float(clean_val)
    except ValueError:
        # Raise a custom validation error for invalid numeric input
        raise ValidationError(f"Invalid numeric input: '{value_str}'")

    # Reject special floating-point values that could cause issues
    if math.isnan(parsed_float) or math.isinf(parsed_float):
        raise ValidationError(
            f"Disallowed value: '{value_str}' (Infinity/NaN not supported)."
        )

    # Enforce configured maximum input limit
    if abs(parsed_float) > Config.MAX_INPUT_VALUE:
        raise ValidationError(
            f"Value exceeds maximum allowed limit of {Config.MAX_INPUT_VALUE}"
        )

    # Return the validated numeric value
    return parsed_float