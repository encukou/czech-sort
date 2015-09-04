# For Python 2, we need to declare the encoding: UTF-8, of course.

from __future__ import unicode_literals

import re
import functools
import unicodedata

try:
    import builtins
except ImportError:
    # Python 2
    import __builtin__ as builtins

def sorted(strings):
    return builtins.sorted(strings, key=key)


nkfd = functools.partial(unicodedata.normalize, 'NFKD')
HACEK = nkfd('č')[-1]


PRIMARY_ALPHABET = dict((nkfd(l), a) for l, a in {
        ' ': ' ',
        '-': ' ',
        '\N{NO-BREAK SPACE}': ' ',
        'a': 'a',
        'b': 'b',
        'c': 'c',
        'č': 'cx',
        'd': 'd',
        'e': 'e',
        'f': 'f',
        'g': 'g',
        'h': 'h',
        'ch': 'hx',
        'i': 'i',
        'j': 'j',
        'k': 'k',
        'l': 'l',
        'm': 'm',
        'n': 'n',
        'o': 'o',
        'p': 'p',
        'q': 'q',
        'r': 'r',
        'ř': 'rx',
        's': 's',
        'š': 'sx',
        't': 't',
        'u': 'u',
        'v': 'v',
        'w': 'w',
        'x': 'x',
        'y': 'y',
        'z': 'z',
        'ž': 'zx',
        "'": '|:',
        '\N{MINUS SIGN}': '|-',
    }.items())

PRIMARY_ALPHABET.update((str(n), '|' + str(n)) for n in range(10))
PRIMARY_ALPHABET.update((n, '~!') for n in '.,;?!:„“”‘’””«»"\'`「」–|\\()/[]()‹›{}<>')
PRIMARY_ALPHABET.update((n, '~$') for n in '@&€£§%‰$')
# Symbols: '~+', straight/curvy (-~), non-/intersecting (!+), no. of lines
PRIMARY_ALPHABET.update((n, '~+-!1') for n in '_')
PRIMARY_ALPHABET.update((n, '~+-!2') for n in '=^')
PRIMARY_ALPHABET.update((n, '~+-+2') for n in '+×')
PRIMARY_ALPHABET.update((n, '~+-+3') for n in '*')
PRIMARY_ALPHABET.update((n, '~+-+4') for n in '#')
PRIMARY_ALPHABET.update((n, '~+~!1') for n in '~')
PRIMARY_ALPHABET.update((n, '~+~!2') for n in '≈')


def primary_alphabet_letter_re(l):
    if l == 'c':
        return 'c(?:(?!h)|$)'
    if l + HACEK in PRIMARY_ALPHABET:
        return '{0}(?:(?!{1})|$)'.format(l, HACEK)
    else:
        return re.escape(l)


PRIMARY_RE = re.compile('|'.join(primary_alphabet_letter_re(l)
                                 for l in PRIMARY_ALPHABET))


def key(string):
    string = re.sub('-(?=\d)', '\N{MINUS SIGN}', string)
    lowercased = string.lower()
    normal = nkfd(lowercased)
    primary = tuple(PRIMARY_ALPHABET[l] for l in PRIMARY_RE.findall(normal))
    is_upper = tuple(c == c.upper() for c in string)
    return primary, normal, is_upper, string
