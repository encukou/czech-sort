# For Python 2, we need to declare the encoding: UTF-8, of course.

from czech_sort import key

inputs = (
    # Two examples from Wikipedia:
    # https://cs.wikipedia.org/wiki/Abecedn%C3%AD_%C5%99azen%C3%AD
    'A B C Č D E F G H Ch I J K L M N O P Q R Ř S Š T U V W X Y Z Ž'.split(),
    ['padá', 'sál', 'sála', 'sálá', 'säla', 'satira', 'si lehá', 'si nese',
     'sílí', 'šála', 'šat', 'ta'],

    # Two examples from 
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

