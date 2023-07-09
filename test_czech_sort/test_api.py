# For Python 2, we need to declare the encoding: UTF-8, of course.

import sqlite3
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


def test_bytes_key_db():
    connection = sqlite3.connect(":memory:")
    try:
        connection.create_function("czech_sort", 1, czech_sort.bytes_key)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE items(name)")
        cursor.executemany("INSERT INTO items VALUES (?)", [(u'sídliště',), (u'shoda',), (u'schody',)])
        connection.commit()
        result = cursor.execute("SELECT name FROM items ORDER BY czech_sort(name)").fetchall()
    finally:
        connection.close()

    assert result == [(u'shoda',), (u'schody',), (u'sídliště',)]


def test_error_bytes():
    with pytest.raises(TypeError):
        czech_sort.sorted([b'a', b'b'])
