import cparsers

AAA = cparsers.many(cparsers.string.word('A'))
BBB = cparsers.many(cparsers.string.word('B'))


PARSERS = {
    'AAA': AAA,
    'BBB': BBB,

    'TES': cparsers.choiceOf(AAA, BBB),
}