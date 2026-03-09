"""Basic and advanced arithmetic operations."""

import math
from app.exceptions import DivisionByZeroError


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference between two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of two numbers."""
    if b == 0:
        # Prevent division by zero
        raise DivisionByZeroError("Cannot divide by zero.")
    return a / b


def power(a: float, b: float) -> float:
    """Return a raised to the power of b."""
    return math.pow(a, b)


def root(a: float, b: float) -> float:
    """Return the b-th root of a."""
    if b == 0:
        # Root degree cannot be zero
        raise DivisionByZeroError("Root degree cannot be zero.")
    return math.pow(a, 1 / b)


def modulus(a: float, b: float) -> float:
    """Return the remainder of a divided by b."""
    if b == 0:
        # Prevent modulo by zero
        raise DivisionByZeroError("Cannot modulo by zero.")
    return a % b


def int_divide(a: float, b: float) -> float:
    """Return the integer division result of a by b."""
    if b == 0:
        # Prevent division by zero
        raise DivisionByZeroError("Cannot divide by zero.")
    return a // b


def percent(a: float, b: float) -> float:
    """Return what percentage a is of b."""
    if b == 0:
        # Prevent percentage calculation with zero divisor
        raise DivisionByZeroError("Cannot calculate percentage with zero divisor.")
    return (a / b) * 100


def abs_diff(a: float, b: float) -> float:
    """Return the absolute difference between two numbers."""
    return abs(a - b)