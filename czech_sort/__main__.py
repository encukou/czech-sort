import sys

import fileinput
from . import impl

lines = fileinput.input()

for line in impl.sorted(lines):
    print(line.rstrip('\n'))
