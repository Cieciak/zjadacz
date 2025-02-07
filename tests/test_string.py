from cparsers.status import Status
from cparsers.string import StringParser
from cparsers.parser import Parser
from cparsers.helpers import *

import cparsers.string

from pprint import pprint

def test_word():
    p = StringParser.word('hello')

    s = Status('hello')

    r = p.run(s)

    assert r.result == 'hello'

def test_regex():
    p = StringParser.regex(r'^[0-9]{2}[a-z]{2}')

    s = Status('24rg')

    r = p.run(s)

    assert r.result == '24rg'

def test_helpers():

    p = cparsers.string.uint()

    s = Status('2137')

    r = p.run(s)

    assert r.result == 2137

    p = cparsers.string.sint()

    s = Status('-3621')

    r = p.run(s)

    assert r.result == -3621

def test_expr():

    integer = cparsers.string.sint()

    add = Parser.ChoiceOf(
        sequenceOf(
            Parser.Lazy(lambda: term), 
            cparsers.string.regex(r'^\+'), 
            Parser.Lazy(lambda: add)
        ).map(lambda s: {'+': [s.result[0], s.result[2]]}),

        Parser.Lazy(lambda: term),
    )

    term = Parser.ChoiceOf(
        sequenceOf(
            Parser.Lazy(lambda: fact),
            cparsers.string.regex(r'^\*'),
            Parser.Lazy(lambda: term)
        ).map(lambda s: {'*': [s.result[0], s.result[2]]}),
        Parser.Lazy(lambda: fact),
    )

    fact = Parser.ChoiceOf(
        sequenceOf(
            cparsers.string.word('('),
            Parser.Lazy(lambda: add),
            cparsers.string.word(')')
        ).map(lambda s: s.result[1]),
        integer,
    )

    s = Status('10+(1+3*6)*(2+1)+6*6+7')
    #s = Status('12+4')

    r = add.run(s)

    assert r.result == {'+': [10, {'+': [{'*': [{'+': [1, {'*': [3, 6]}]}, {'+': [2, 1]}]}, {'+': [{'*': [6, 6]}, 7]}]}]}

def test_expr_eval():

    integer = cparsers.string.sint()

    add = Parser.ChoiceOf(
        sequenceOf(
            Parser.Lazy(lambda: term),
            cparsers.string.word('+'),
            Parser.Lazy(lambda: add),
        ).map(lambda s: s.result[0] + s.result[2]),

        Parser.Lazy(lambda: term),
    )

    term = Parser.ChoiceOf(
        sequenceOf(
            Parser.Lazy(lambda: fact),
            cparsers.string.word('*'),
            Parser.Lazy(lambda: term),
        ).map(lambda s: s.result[0] * s.result[2]),

        Parser.Lazy(lambda: fact),
    )

    fact = Parser.ChoiceOf(
        sequenceOf(
            cparsers.string.word('('),
            Parser.Lazy(lambda: add),
            cparsers.string.word(')'),
        ).map(lambda s: s.result[1]),

        integer,
    )

    text = '10+(1+3*6)*(2+1)+6*6+7+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1'

    s = Status(text)

    r = add.run(s)

    assert r.result == eval(text)