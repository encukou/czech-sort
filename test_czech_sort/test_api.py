# For Python 2, we need to declare the encoding: UTF-8, of course.

import pytest

import czech_sort


def test_sorted():
    result = czech_sort.sorted([u'sídliště', u'shoda', u'schody'])
    assert result == [u'shoda', u'schody', u'sídliště']


def test_key():
    result = sorted([u'sídliště', u'shoda', u'schody'], key=czech_sort.key)
    assert result == [u'shoda', u'schody', u'sídliště']


def test_bytes_key():
    result = sorted([u'sídliště', u'shoda', u'schody'], key=czech_sort.bytes_key)
    assert result == [u'shoda', u'schody', u'sídliště']


def test_error_bytes():
    with pytest.raises(TypeError):
        czech_sort.sorted([b'a', b'b'])
