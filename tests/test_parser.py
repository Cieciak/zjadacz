from cparsers.status  import Status
from cparsers.error   import ParserError
from cparsers.parser  import Parser
from cparsers.helpers import *
from cparsers import string

def test_parser():
    parser = simplex("hello")
    result = parser.run(Status(["hello"]))

    assert result.result == "hello"

def test_parser_sequence():
    sequence = sequenceOf(
        simplex("hello"),
        simplex("world"),
    )

    result = sequence.run(Status(["hello", "world"]))
    assert result.result == ["hello", "world"]

def test_parser_choice():
    p = sequenceOf(
        choiceOf(
            simplex("milk"),
            simplex("brown"),
        ),
        simplex("chocolate"),
    )

    r = p.run(Status(["milk", "chocolate"]))
    assert r.result == ["milk", "chocolate"]

    r = p.run(Status(["brown", "chocolate"]))
    assert r.result == ["brown", "chocolate"]

    r = p.run(Status(["spicy", "chocolate"]))
    assert type(r) == ParserError


def test_parser_many():
    p = sequenceOf(
        many(
            simplex("egg"),
        ),
        simplex('goat')
    )
    r = p.run(Status(["egg", "egg", "egg", 'goat']))
    assert r.result == [["egg", "egg", "egg"], 'goat']

    parser = many(
        simplex('egg'),
    )

    status = Status([])

    result = parser.run(status)

    assert result.result == []

def test_parser_strict_many():
    p = many(
        simplex("egg"),
        strict = True,
    )

    r = p.run(Status(["egg", "egg", "egg"]))
    assert r.result == ["egg", "egg", "egg"]

    r = p.run(Status([]))
    assert type(r) == ParserError

def test_parser_map():
    p = sequenceOf(
        simplex("["),
        simplex("egg"),
        simplex("]"),
    ).map(lambda s: s.result[1])

    r = p.run(Status(["[", "egg", "]"]))
    assert r.result == "egg"

def test_parser_chain():
    def transformer(s: Status) -> Status:
        if len(s.head) == 0: return ParserError("Unexpected EOF")
        flag = isinstance(s.head[0], str)
        if flag: return s.chainResult(s.head[0], increment=1)
        return ParserError("[{s.head[0]}] is not a string")

    String = Parser(transformer)

    def selector(s: Status) -> Parser:
        if   s.result == "hello": return simplex("world")
        elif s.result == "spam": return many(simplex("egg"), strict=True)

    p = String.chain(selector)
    r = p.run(Status(["hello", "world"]))
    assert r.result == "world"

    r = p.run(Status(["spam", "egg", "egg"]))

    assert r.result == ["egg", "egg"]

def test_between():
    b = between(simplex("["), simplex("]"))

    e = b(simplex("hiss"))

    r = e.run(Status(["[", "hiss", "]"]))

    assert r.result == "hiss"

def test_separeted():
    s = separated(simplex(","))

    p = s(simplex("eggs"))

    r = p.run(Status(["eggs", ",", "eggs", ",", "eggs"]))

    assert r.result == ["eggs", "eggs", "eggs"]

def test_optional():
    data = "hello     world"

    p = sequenceOf(
        string.word("hello"),
        string.word(" "),
        optional(
            string.regex(" +")
        ),
        string.word("world"),
    ).map(
        lambda s: (s.result[0], s.result[3])
    )

    r = p.run(Status(data))

    assert r.result == ('hello', 'world')

def test_match():

    data = "d20:12\ncoin:heads\noracle:yes\n"

    cases = {
        'd20': string.uint(),
        'coin': choiceOf(string.word('heads'), string.word('tails')),
        'oracle': choiceOf(string.word('yes'), string.word('no')),
    }

    key_val_parser = sequenceOf(string.regex('[a-z0-9]+'), string.word(':')).map(lambda s: s.result[0]).match(cases)

    many_parser = many(sequenceOf(key_val_parser, string.word('\n')).map(lambda s: s.result[0]))

    r = many_parser.run(Status(data))

    assert r.result == [12, 'heads', 'yes']