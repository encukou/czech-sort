import pytest

import czech_sort


def test_sorted():
    result = czech_sort.sorted(['sídliště', 'shoda', 'schody'])
    assert result == ['shoda', 'schody', 'sídliště']


def test_key():
    result = sorted(['sídliště', 'shoda', 'schody'], key=czech_sort.key)
    assert result == ['shoda', 'schody', 'sídliště']


def test_error_bytes():
    with pytest.raises(TypeError):
        czech_sort.sorted([b'a', b'b'])
