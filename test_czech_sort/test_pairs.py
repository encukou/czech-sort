# For Python 2, we need to declare the encoding: UTF-8, of course.

from __future__ import unicode_literals

from czech_sort import key

inputs = (
    # Examples from Wikipedia:
    # https://cs.wikipedia.org/wiki/Abecedn%C3%AD_%C5%99azen%C3%AD
    [' '] + '-'.split() +
     'A B C Č D E F G H Ch I J K L M N O P Q R Ř S Š T U V W X Y Z Ž'.split() +
     '0 1 2 3 4 5 6 7 8 9 \''.split() +
     [],

    ['padá', 'sál', 'sála', 'sálá', 'säla', 'satira', 'si lehá', 'si nese',
     'sílí', 'šála', 'šat', 'ta'],

    'ȧ á ā à â ǎ ã ă ȃ ą å ä a̋ ȁ'.split(),

    # Examples from ÚJČ AV ČR:
    # http://prirucka.ujc.cas.cz/?action=view&id=900
    ['shoda', 'schody', 'sídliště'],
    ['motýl noční', 'motýlek'],
    ['damašek', 'Damašek'],
    ['da capo', 'ďábel', 'dabing', 'ucho', 'úchop', 'uchopit'],
    ['kanon', 'kanón', 'kaňon', 'kánon'],
    'á ď é ě í ň ó ť ú ů ý'.split(),
    # XXX (misplaced ł): 'à â ä ç è ê ĺ ľ ł ô ö ŕ ü ż'.split(),
    'à â ä ç è ê ĺ ľ ô ö ŕ ü ż'.split(),
    'C Ç °C'.split(),
    # XXX: 'C Ç °C X Xⁿ Xₑ Xⁿₑ'.split(),
    'ZZ Z-2 Ž 3 3N 3no 5A 8'.split(),
    # XXX: Symbols

    # Others
    ['cyp', 'čáp', 'čupřina'],
    ['Cyp', 'Čáp', 'Čupřina'],
    ['CYP', 'ČÁP', 'ČUPŘINA'],
)


def get_pairs(inputs):
    for input in inputs:
        for i, first in enumerate(input):
            for second in input[i+1:]:
                yield first, second


def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ == 'test_pair':
        metafunc.parametrize(
            ['a', 'b'],
            list(get_pairs(inputs)))


def test_pair(a, b):
    ka = key(a)
    kb = key(b)
    assert ka <= kb
    assert not ka > kb
    if a == b:
        assert ka == kb
        assert ka >= kb
        assert not ka < kb
        assert not ka != kb
    else:
        assert not ka == kb
        assert not ka >= kb
        assert ka < kb
        assert ka != kb
