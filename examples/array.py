from sys import argv

from cparsers import *

#
# ELEMENT ::= | SINT
#             | ARRAY
#

element = choiceOf(
    sint(),
    lazy(lambda: array)
)

#
# ARRAY ::= "[" sepby(",")(ELEMENT) "]"
#

array = sequenceOf(
    word('['),
    separated(word(','))(element),
    word(']'),
).map(lambda s: s.result[1])

if __name__ == '__main__':
    s = Status('[1,[2],3]')

    r = array.run(s)

    print(r)