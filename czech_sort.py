import re
import builtins
import functools
import unicodedata

__all__ = ['sorted', 'key']

def sorted(strings):
    return builtins.sorted(strings, key=key)

def key(string):
    words = string.split()
    return tuple(word_key(w) for w in words)


nkfd = functools.partial(unicodedata.normalize, 'NFKD')
HACEK = nkfd('č')[-1]


PRIMARY_ALPHABET = {nkfd(l): a for l, a in {
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
    }.items()}


def primary_alphabet_letter_re(l):
    if l == 'c':
        return 'c(?:(?!h)|$)'
    if l + HACEK in PRIMARY_ALPHABET:
        return '{}(?:(?!{})|$)'.format(l, HACEK)
    else:
        return l


PRIMARY_RE = re.compile('|'.join(primary_alphabet_letter_re(l)
                                 for l in PRIMARY_ALPHABET))


def word_key(word):
    lowercased = word.lower()
    normal = nkfd(lowercased)
    primary = tuple(PRIMARY_ALPHABET[l] for l in PRIMARY_RE.findall(normal))
    return primary, normal, word
