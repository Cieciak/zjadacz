import zjadacz

AAA = zjadacz.many(zjadacz.string.word('A'))
BBB = zjadacz.many(zjadacz.string.word('B'))


PARSERS = {
    'AAA': AAA,
    'BBB': BBB,

    'TES': zjadacz.choiceOf(AAA, BBB),
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