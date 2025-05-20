import cparsers

AAA = cparsers.many(cparsers.string.word('A'))
BBB = cparsers.many(cparsers.string.word('B'))


PARSERS = {
    'AAA': AAA,
    'BBB': BBB,

    'TES': cparsers.choiceOf(AAA, BBB),
}

def mul(arr):
    v = 0
    for i in arr.result:
        v = 10 * v + int(i)

    return v

MAPS = {
    'fromdigits': mul,
    'firstelement': lambda s: s.result[0],
    'secondelement': lambda s: s.result[1], 
}