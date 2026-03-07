import pytest
from app.operations import add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff
from app.exceptions import DivisionByZeroError


# Test addition with positive, negative, zero, and float values
@pytest.mark.parametrize("a, b, expected", [
    (5, 5, 10), 
    (-2, 3, 1), 
    (0, 0, 0), 
    (2.5, 2.5, 5.0)
])
def test_add(a, b, expected): 
    assert add(a, b) == expected


# Test subtraction across different numeric cases
@pytest.mark.parametrize("a, b, expected", [
    (10, 5, 5), 
    (0, 5, -5), 
    (-5, -5, 0)
])
def test_subtract(a, b, expected): 
    assert subtract(a, b) == expected


# Test multiplication with integers and floats
@pytest.mark.parametrize("a, b, expected", [
    (5, 5, 25), 
    (-2, 3, -6), 
    (1.5, 2.0, 3.0)
])
def test_multiply(a, b, expected): 
    assert multiply(a, b) == expected


# Test division including negative numbers, repeating decimals, and zero numerator
@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0), 
    (-10, 2, -5.0), 
    (1, 3, 0.3333333333333333),
    (0, 10, 0.0)    # Zero numerator
])
def test_divide(a, b, expected): 
    # Use approx to handle floating-point precision differences
    assert divide(a, b) == pytest.approx(expected)


# Test exponentiation including edge cases (negative exponent, zero base)
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 8), 
    (5, 0, 1), 
    (9, 0.5, 3),
    (2, -1, 0.5),   # Negative exponent
    (-2, 3, -8),    # Negative base
    (0, 5, 0)       # Zero base
])
def test_power(a, b, expected): 
    assert power(a, b) == expected


# Test nth-root calculations
@pytest.mark.parametrize("a, b, expected", [
    (8, 3, 2), 
    (9, 2, 3)
])
def test_root(a, b, expected): 
    assert root(a, b) == expected


# Test modulus with integers, floats, and negative values
@pytest.mark.parametrize("a, b, expected", [
    (10, 3, 1), 
    (10.5, 3, 1.5), 
    (-10, 3, 2),
    (10, 2.5, 0.0)  # Decimal divisor
])
def test_modulus(a, b, expected): 
    assert modulus(a, b) == expected


# Test integer (floor) division behavior
@pytest.mark.parametrize("a, b, expected", [
    (10, 3, 3), 
    (10, 4, 2), 
    (-10, 3, -4),
    (10.5, 2.5, 4.0) # Decimal division
])
def test_int_divide(a, b, expected): 
    assert int_divide(a, b) == expected


# Test percentage calculation including repeating decimals
@pytest.mark.parametrize("a, b, expected", [
    (50, 100, 50.0), 
    (1, 4, 25.0),
    (0, 100, 0.0),  # Zero percent
    (1, 3, 33.33333333333333) # Repeating decimal
])
def test_percent(a, b, expected): 
    # Use approx to avoid floating-point precision issues
    assert percent(a, b) == pytest.approx(expected)


# Test absolute difference between two numbers
@pytest.mark.parametrize("a, b, expected", [
    (10, 5, 5), 
    (5, 10, 5), 
    (-5, 5, 10), 
    (-5, -10, 5)
])
def test_abs_diff(a, b, expected): 
    assert abs_diff(a, b) == expected


# Ensure operations that divide by the second operand raise errors when b = 0
@pytest.mark.parametrize("operation", [divide, root, modulus, int_divide, percent])
def test_zero_division_errors(operation):
    
    # All division-based operations should raise DivisionByZeroError
    with pytest.raises(DivisionByZeroError):
        operation(10, 0)