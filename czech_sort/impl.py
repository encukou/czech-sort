# For Python 2, we need to declare the encoding: UTF-8, of course.

"""
The ``czech_sort`` library provides utilities for quick-and-dirty string
comparisons, using the Czech alphabetization rules.

Future versions of this library may change the sort order, as more details
and exotic characters are added.
"""

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
    """Return a list of strings sorted using Czech collation

    :param strings: iterable of strings (unicode in Python 2)
    """
    return builtins.sorted(strings, key=key)


nfkd = functools.partial(unicodedata.normalize, 'NFKD')
HACEK = nfkd('č')[-1]


def key(string):
    """Return a Czech sort key for the given string

    :param string: string (unicode in Python 2)

    Comparing the sort keys of two strings will give the result according
    to how the strings would compare in Czech collation order, i.e.
        ``key(s1) < key(s2)``  <=>  ``s1`` comes before ``s2``

    The structure of the sort key may change in the future.
    The only operations guaranteed to work on it are comparisons and equality
    checks (<, ==, etc.) against other keys.
    """
    # The multi-level key is a nested tuple containing strings and ints.
    # The tuple contains sub-keys that roughly correspond to levels in
    # UTS #10 (http://unicode.org/reports/tr10/). Except for fallback strings
    # at the end, each contains a tuple of typically one key per element/letter.
    # - Alphabet:
    #    Separators (0, p, l, w)
    #       p: -no. of paragraph separators
    #       l: -no. of line separators
    #       w: -no. of word separators (spaces)
    #    Letters (1, l); l is the base letter, lowercased
    #       Special letters: 'č' shows up as 'cx'; 'ř' as 'rx', etc.
    #                        the 'ch' digraph becomes 'hx'
    #    Numbers (2, n); n is int(numeric value * 100)
    #    Missing for non-letters
    # - Diacritics (p, n, s)
    #    p: position (above, below, behind, in front, in/over/around, unknown)
    #       (as a sorted tuple of indices)
    #    s: shape (dot, grave, breve, ..., unknown)
    #       (as a sorted tuple of indices)
    #    Missing for non-letters; empty if diacritics included in base (e.g. ř)
    # - Case: True for uppercased letters
    #    Missing for non-letters
    # - Punctuation: see PUNCTUATION_MAP below
    # - (fallback) NFKD-normalized string
    # - (fallback) original string

    subkeys = [], [], [], []
    add_alphabet = subkeys[0].append
    add_diacritic = subkeys[1].append
    add_case = subkeys[2].append
    add_punctuation = subkeys[3].append
    skip = 0
    normal = nfkd(string).rstrip()
    diacritics = []
    for i, char in enumerate(normal):
        if skip > 0:
            skip -= 1
            continue
        category = get_category(char)
        cat0, cat1 = category
        if cat0 == 'L':
            # Letter (Lowercase, Modifier, Other, Titlecase, Uppercase)
            char_lower = char.lower()
            found = False
            if char_lower in DECOMPOSING_EXTRAS:
                # stuff like Ł doesn't decompose in Unicode; do it manually
                char_lower, _extra_diacritics = DECOMPOSING_EXTRAS[char_lower]
                diacritics.extend(_extra_diacritics)
            for next in normal[i+1:]:
                if next == HACEK and char_lower in ('c', 'r', 's', 'z'):
                    skip += 1
                    char_lower = char_lower + 'x'
                elif char_lower == 'c' and next.lower() == 'h':
                    skip += 1
                    char_lower = 'hx'
                    break
                elif next in DIACRITICS_MAP:
                    skip += 1
                    diacritics.extend(DIACRITICS_MAP[next])
                elif unicodedata.category(char)[0] == 'M':
                    skip += 1
                    diacritics.append((POS_UNKNOWN, SH_UNKNOWN))
                else:
                    break
            add_alphabet((1, char_lower))
            if diacritics:
                add_diacritic(make_diacritics_key(diacritics))
            else:
                add_diacritic(())
            add_case(cat1 in ('u', 't'))  # upper & title case
            add_punctuation((0, ))
            diacritics = []
        elif cat0 == 'Z':
            # Separator (Line, Paragraph, Space)
            counts = {'Zp': 0, 'Zl': 0, 'Zs': 0}
            counts[category] = 1
            for next in normal[i+1:]:
                next_cat = get_category(next)
                if next_cat[0] == 'Z':
                    counts[next_cat] += 1
                    skip += 1
                else:
                    break
            add_alphabet((0, -counts['Zp'], -counts['Zl'], -counts['Zs']))
            add_diacritic(())
            add_case(False)
            add_punctuation((0, ))
        elif char in DIACRITICS_BEFORE_MAP:
            diacritics.extend(DIACRITICS_BEFORE_MAP[char])
        elif char in DIACRITICS_MAP:
            diacritics.extend(DIACRITICS_MAP[char])
        elif char in PUNCTUATION_MAP:
            add_punctuation(PUNCTUATION_MAP[char])
        elif cat0 == 'P':
            # Punctuation (Connector, Dash, Open/Close, Final/Initial Quote, Other)
            add_punctuation((3, ))
        elif cat0 == 'N':
            # Number (Decimal digit, Letter, Other)
            add_alphabet((2, int(unicodedata.numeric(char, 0)) * 100))
            add_diacritic(())
            add_case(False)
            add_punctuation((0, ))
        elif cat0 == 'S':
            # Symbol (Currency, Modifier, Math)
            add_punctuation((3, ))
        elif cat0 == 'C':
            # Other (Control, Format, Not Assigned, Private Use, Surrogate)
            pass
        elif cat0 == 'M':
            # Mark (Spacing Combining, Enclosing, Nonspacing)
            # TODO
            diacritics.append((POS_FRONT, SH_UNKNOWN))
        else:
            raise ValueError('Unknown Unicode category')
    if diacritics:
        add_diacritic(make_diacritics_key(diacritics))
        diacritics = []
    return tuple(tuple(k) for k in subkeys) + (normal, string)


def make_diacritics_key(diacritics):
    positions, shapes = zip(*diacritics)
    positions = tuple(builtins.sorted(positions))
    shapes = tuple(builtins.sorted(shapes))
    return positions, shapes


def get_category(c):
    return CATEGORY_CORRECTIONS.get(c, unicodedata.category(c))

# Treat \n as a line separator
CATEGORY_CORRECTIONS = {'\n': 'Zl'}

POS_ABOVE, POS_BELOW, POS_BEHIND, POS_FRONT, POS_IN, POS_UNKNOWN = range(6)
(SH_DOT, SH_ACUTE, SH_HORIZONTAL, SH_VERTICAL, SH_GRAVE, SH_CIRCUMFLEX,
 SH_HACEK, SH_TILDE, SH_BREVE, SH_INV_BREVE, SH_HOOK, SH_RING,
 SH_UNKNOWN) = range(13)

DIACRITICS_MAP = {
    "'": [(POS_BEHIND, SH_VERTICAL)],
    '\N{PRIME}': [(POS_BEHIND, SH_VERTICAL)],
    '\N{APOSTROPHE}': [(POS_BEHIND, SH_VERTICAL)],
    '\N{COMBINING DOT ABOVE}': [(POS_ABOVE, SH_DOT)],
    '\N{COMBINING ACUTE ACCENT}': [(POS_ABOVE, SH_ACUTE)],
    '\N{COMBINING MACRON}': [(POS_ABOVE, SH_HORIZONTAL)],
    '\N{COMBINING GRAVE ACCENT}': [(POS_ABOVE, SH_GRAVE)],
    '\N{COMBINING CIRCUMFLEX ACCENT}': [(POS_ABOVE, SH_CIRCUMFLEX)],
    '\N{COMBINING CARON}': [(POS_ABOVE, SH_HACEK)],
    '\N{COMBINING TILDE}': [(POS_ABOVE, SH_TILDE)],
    '\N{COMBINING BREVE}': [(POS_ABOVE, SH_BREVE)],
    '\N{COMBINING INVERTED BREVE}': [(POS_ABOVE, SH_INV_BREVE)],
    '\N{COMBINING HOOK ABOVE}': [(POS_ABOVE, SH_HOOK)],
    '\N{COMBINING RING ABOVE}': [(POS_ABOVE, SH_RING)],

    '\N{COMBINING DOUBLE ACUTE ACCENT}': [(POS_ABOVE, SH_ACUTE)] * 2,
    '\N{COMBINING DOUBLE GRAVE ACCENT}': [(POS_ABOVE, SH_GRAVE)] * 2,
    '\N{COMBINING DIAERESIS}': [(POS_ABOVE, SH_DOT)] * 2,

    '\N{COMBINING OGONEK}': [(POS_BELOW, SH_HOOK)],

    # XXX: All the others
}

DIACRITICS_BEFORE_MAP = {
    "'": [(POS_FRONT, SH_VERTICAL)],
    '\N{PRIME}': [(POS_FRONT, SH_VERTICAL)],
    '\N{APOSTROPHE}': [(POS_FRONT, SH_VERTICAL)],
    '\N{DEGREE SIGN}': [(POS_FRONT, SH_RING)],
}

DECOMPOSING_EXTRAS = {
    'ł': ('l', [(POS_IN, SH_GRAVE)]),
    'ø': ('o', [(POS_IN, SH_GRAVE)]),
}


PUNCTUATION_MAP = {}
# Punctuation key is (0, ) for non-punctuation.
# For punctuation, it can be:
# Hyphen: (-1, )
PUNCTUATION_MAP['-'] = (-1, )
# Marks: (1, i): .,;?!: quotes –|/\()[]()‹›<>{}
#   i: index in the list
for i, c in enumerate('.,;?!:„“”‘’””«»"\'`「」—–|\\()/[]()‹›{}<>'):
    PUNCTUATION_MAP[c] = (1, i)
# Symbols: (2, i): @&€£§%‰$
for i, c in enumerate('@&€£§%‰$'):
    PUNCTUATION_MAP[c] = (2, i)
# Graphics: (3, a, b, n):
#   a: True for curves
#   b: True for overlapping strokes
#   n: number of strokes
PUNCTUATION_MAP['_'] = (3, False, False, 1)
PUNCTUATION_MAP['='] = (3, False, False, 2)
PUNCTUATION_MAP['^'] = (3, False, False, 2)
PUNCTUATION_MAP['+'] = (3, False, True, 2)
PUNCTUATION_MAP['×'] = (3, False, True, 2)
PUNCTUATION_MAP['*'] = (3, False, True, 3)
PUNCTUATION_MAP['#'] = (3, False, True, 4)
PUNCTUATION_MAP['~'] = (3, True, False, 1)
PUNCTUATION_MAP['≈'] = (3, True, False, 2)
# Unknown: (3,)
# XXX: Geometric shapes: (4, n); n is no. of points
