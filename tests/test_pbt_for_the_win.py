import pytest
from hypothesis import given, settings
from hypothesis.strategies import integers
from datetime import timedelta
import math

def simplify_sqrt(radicand):
    if radicand == 0:
        return (0, 0)
    for i in range(radicand // 2, 1, -1):
        if radicand % (i*i) == 0:
            return i, radicand // (i*i)
    return (1, radicand)


@pytest.mark.parametrize(
    "radicand,outcome",
    [
        [0, (0, 0)],
        [1, (1, 1)],
        [2, (1, 2)],
        [4, (2, 1)],
        [9, (3, 1)],
        [12, (2, 3)],
    ]
)
def test_simplify_sqrt(radicand, outcome):
    
    assert simplify_sqrt(radicand) == outcome


@settings(max_examples=1000, deadline=timedelta(milliseconds=50))
@given(integers(min_value=1, max_value=32_000))
def test_radiand_is_not_divisible(radicand):
    n, r = simplify_sqrt(radicand)

    assert simplify_sqrt(r) == (1, r)
