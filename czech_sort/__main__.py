import sys

import fileinput
from . import impl

lines = fileinput.input()

if sys.version_info < (3, 0):
    lines = (l.decode('utf-8') for l in lines)

for line in impl.sorted(lines):
    print(line.rstrip('\n'))
