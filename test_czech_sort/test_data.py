# For Python 2, we need to declare the encoding: UTF-8, of course.

from __future__ import unicode_literals

import sys

from hypothesis import given
from hypothesis.strategies import text

import czech_sort


inputs = (
    # Examples from Wikipedia:
    # https://cs.wikipedia.org/wiki/Abecedn%C3%AD_%C5%99azen%C3%AD
    [' '] + '-'.split() +
     'A B C Č D E F G H Ch I J K L M N O P Q R Ř S Š T U V W X Y Z Ž'.split() +
     '0 1 2 3 4 5 6 7 8 9'.split() +
     [],
    'a á b c č d ď e é ě f g h ch i í j k l m n ň o ó p q r ř s š t ť u ú ů v w x y ý z ž'.split(),

    ['padá', 'sál', 'sála', 'sálá', 'säla', 'satira', 'si lehá', 'si nese',
     'sílí', 'šála', 'šat', 'ta'],

    # Examples from ÚJČ AV ČR:
    # http://prirucka.ujc.cas.cz/?action=view&id=900
    ['shoda', 'schody', 'sídliště'],
    ['motýl noční', 'motýlek'],
    ['damašek', 'Damašek'],
    ['da capo', 'ďábel', 'dabing', 'ucho', 'úchop', 'uchopit'],
    ['kanon', 'kanón', 'kaňon', 'kánon'],
    'á ď é ě í ň ó ť ú ů ý'.split(),
    'à â ä ç è ê ĺ ľ ł ô ö ŕ ü ż'.split(),
    'C Ç °C'.split(),
    # XXX: 'C Ç °C X Xⁿ Xₑ Xⁿₑ'.split(),
    'ZZ Z-2 Ž 3 3N 3no 5A 8'.split(),
    # XXX: Symbols
    '@&€£§%‰$',

    # Others
    ['cyp', 'Cyp', 'CYP', 'čáp', 'Čáp', 'ČÁP', 'čupřina', 'Čupřina', 'ČUPŘINA'],
    ['goa uld', 'goa xyz', 'goa-uld', 'goauld', 'goàuld', "goa'uld", 'goa-xyz'],
    ['mac', 'mác', 'mah', 'máh', 'mach', 'mách', 'máchl', 'moh'],
    "ȧ á ā à â ǎ ã ă ȃ å ä a̋ ȁ ą a' °a".split(),
    ['', ' ', '-', "'"],
    ['è', 'ê', 'ề'],
    ['a\n b', 'a \nb', 'a\nb', 'a b', 'ab'],
    ['Ļ', 'Ł', 'M', 'Ơ', 'Ø', 'P'],
)


def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ == 'test_sorted':
        metafunc.parametrize(
            'l', [list(l) for l in inputs])
    if metafunc.function.__name__ in ('test_key', 'test_bytes_key'):
        metafunc.parametrize(
            's', [c for l in inputs for c in l])


def test_sorted(l):
    result = czech_sort.sorted(reversed(l))
    print('exp:', l)
    print('got:', result)
    assert l == result


def test_key(s):
    """Assert keys are immutable and well ordered"""
    # Actually, this is a strict type check
    key = czech_sort.key(s)
    check_key_type(key)


def check_key_type(t):
    if type(t) in (str, int, bool):
        return True
    if sys.version_info < (3, 0) and type(t) is unicode:
        return True
    if type(t) is tuple:
        for c in t:
            check_key_type(c)
        return
    raise AssertionError('{0} is a {1}'.format(t, type(t)))


def test_bytes_key(s):
    """Assert keys are immutable and well ordered"""
    # Actually, this is a strict type check
    key = czech_sort.bytes_key(s)


def check_bytes_key_type(b):
    if sys.version_info < (3, 0) and type(t) is str:
        return True
    if type(b) is bytes:
        return True
    raise AssertionError('{0} is a {1}'.format(b, type(b)))


@given(random_string=text())
def test_sorted_hypothesis(random_string):
    result = czech_sort.sorted(random_string)
    assert type(result) == list


@given(random_string=text())
def test_key_hypothesis(random_string):
    # Actually, this is a strict type check
    key = czech_sort.key(random_string)
    check_key_type(key)


@given(random_string=text())
def test_bytes_key_hypothesis(random_string):
    # Actually, this is a strict type check
    key = czech_sort.bytes_key(random_string)
    check_bytes_key_type(key)
