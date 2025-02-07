from sys import argv

from cparsers.status import Status
from cparsers import string
from cparsers.parser import Parser

add = Parser.ChoiceOf(
    Parser.SequenceOf(
        Parser.Lazy(lambda: mul),
        string.regex(r'^[\+\-]'),
        Parser.Lazy(lambda: add),
    ).map(lambda s: s.result[0] + s.result[2] if s.result[1] == '+' else s.result[0] - s.result[2]),

    Parser.Lazy(lambda: mul)
)

mul = Parser.ChoiceOf(
    Parser.SequenceOf(
        Parser.Lazy(lambda: fact),
        string.regex(r'^[\*\/]'),
        Parser.Lazy(lambda: mul),
    ).map(lambda s: s.result[0] * s.result[2] if s.result[1] == '*' else s.result[0] / s.result[2]),

    Parser.Lazy(lambda: fact)
)

fact = Parser.ChoiceOf(
    Parser.SequenceOf(
        string.word('('),
        Parser.Lazy(add),
        string.word(')'),
    ).map(lambda s: s.result[1]),

    string.sint()
)

s = Status(argv[1])

r = add.run(s)

print(r.result)