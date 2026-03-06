import pytest
from app.operations import add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff
from app.exceptions import DivisionByZeroError

@pytest.mark.parametrize("a, b, expected", [(5, 5, 10), (-2, 3, 1), (0, 0, 0), (2.5, 2.5, 5.0)])
def test_add(a, b, expected): assert add(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [(10, 5, 5), (0, 5, -5), (-5, -5, 0)])
def test_subtract(a, b, expected): assert subtract(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [(5, 5, 25), (-2, 3, -6), (1.5, 2.0, 3.0)])
def test_multiply(a, b, expected): assert multiply(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [(10, 2, 5.0), (-10, 2, -5.0), (1, 3, 0.3333333333333333)])
def test_divide(a, b, expected): assert divide(a, b) == pytest.approx(expected)

@pytest.mark.parametrize("a, b, expected", [(2, 3, 8), (5, 0, 1), (9, 0.5, 3)])
def test_power(a, b, expected): assert power(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [(8, 3, 2), (9, 2, 3)])
def test_root(a, b, expected): assert root(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [(10, 3, 1), (10.5, 3, 1.5), (-10, 3, 2)])
def test_modulus(a, b, expected): assert modulus(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [(10, 3, 3), (10, 4, 2), (-10, 3, -4)])
def test_int_divide(a, b, expected): assert int_divide(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [(50, 100, 50.0), (1, 4, 25.0)])
def test_percent(a, b, expected): assert percent(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [(10, 5, 5), (5, 10, 5), (-5, 5, 10), (-5, -10, 5)])
def test_abs_diff(a, b, expected): assert abs_diff(a, b) == expected

# Zero Division Exceptions
@pytest.mark.parametrize("operation", [divide, root, modulus, int_divide, percent])
def test_zero_division_errors(operation):
    with pytest.raises(DivisionByZeroError):
        operation(10, 0)