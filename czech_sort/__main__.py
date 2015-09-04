import fileinput
from . import impl


for line in impl.sorted(fileinput.input()):
    print(line.rstrip('\n'))
