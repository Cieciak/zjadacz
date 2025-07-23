import pytest

from cparsers.status  import Status
from cparsers.error   import ParserError
from cparsers.parser  import Parser
from cparsers.helpers import *
from cparsers import string

def test_future_parser():
    with pytest.raises(RuntimeError) as err_info:
        parser = future()
        parser.run(Status('hello'))

    assert err_info.value.args[0] == 'transformer is not defined'

def test_future_parser_assignment():

    parser = future()

    with pytest.raises(RuntimeError) as err_info:
        parser.run(Status('hello'))

    assert err_info.value.args[0] == 'transformer is not defined'

    parser.reassign(string.word('hello'))
    r = parser.run(Status('hello'))

    assert r.result == 'hello'

def test_future_recursion():

    parser = future()

    recurent = sequenceOf(
        string.word('r'),
        choiceOf(
            string.word('.'),
            parser,
        )
    ).map(
        lambda s: [s.result[0], ] + s.result[1] if type(s.result[1]) == list else s.result
    )

    parser.reassign(recurent)

    r = parser.run(Status('rrrr.'))

    assert r.result == ['r', 'r', 'r', 'r', '.']

def test_future_array():

    array_parser = future()

    element_parser = choiceOf(
        string.sint(),
        array_parser,
    )

    array_parser.reassign(
        sequenceOf(
            string.word('['),
            separated(string.word(','))(element_parser),
            string.word(']')
        ).map(lambda s: s.result[1])
    )

    s = Status('[1,[2,3],4,[5,6,7],[8,[9,10]]]')

    r = array_parser.run(s)

    assert r.result == [1, [2,3], 4, [5, 6, 7], [8, [9,10]]]