from cparsers.error import ParserError

def test_error():
    err = ParserError("test")
    assert err.__repr__() == "Parser Error: test"

def test_trace():
    src = ParserError("src")

    err = ParserError.propagate("local", src)

    assert err.trace == [src, ]
