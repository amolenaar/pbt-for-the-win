import pytest
import hypothesis

from pbt_for_the_win import __version__


def simplify_sqrt(radicand):
    if radicand < 1:
        return None
    for i in range(radicand // 2, 1, -1):
        if radicand % (i*i) == 0:
            return i, radicand // (i*i)
    return (1, radicand)

@pytest.mark.parametrize(
    "radicand,outcome",
    [
        [2, (1, 2)],
        [4, (2, 1)],
        [9, (3, 1)],
        [12, (2, 3)],
    ]
)
def test_simplify_sqrt(radicand, outcome):
    
    assert simplify_sqrt(radicand) == outcome

