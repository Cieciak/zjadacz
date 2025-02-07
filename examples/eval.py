from sys import argv

from cparsers import *

##
## ADD ::= | MUL [+-] ADD
##         | MUL
##
add = choiceOf(
    sequenceOf(
        lazy(lambda: mul),
        string.regex(r'^[\+\-]'),
        lazy(lambda: add),
    ).map(lambda s: s.result[0] + s.result[2] if s.result[1] == '+' else s.result[0] - s.result[2]),

    lazy(lambda: mul)
)

##
## MUL ::= | FACT [*/] MUL
##         | FACT
##
mul = choiceOf(
    sequenceOf(
        lazy(lambda: fact),
        string.regex(r'^[\*\/]'),
        lazy(lambda: mul),
    ).map(lambda s: s.result[0] * s.result[2] if s.result[1] == '*' else s.result[0] / s.result[2]),

    lazy(lambda: fact)
)

##
## FACT ::= | ( ADD )
##          | SINT
##
fact = choiceOf(
    sequenceOf(
        string.word('('),
        lazy(lambda: add),
        string.word(')'),
    ).map(lambda s: s.result[1]),

    string.sint()
)

if __name__ == '__main__':
    ...