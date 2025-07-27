import zjadacz

from zjadacz import Status
from zjadacz import byte

def test_byte_word():

    parser = byte.word(b'test')

    status_bytearray = Status(bytearray('test', 'utf-8'))
    status_bytes     = Status(bytes('test', 'utf-8'))
    status_bytestr   = Status(b'test')

    result_bytearray = parser.run(status_bytearray)
    result_bytes     = parser.run(status_bytes)
    result_bytestr   = parser.run(status_bytestr)

    assert type(result_bytes.result) == bytes

    assert result_bytearray.result == bytearray('test', 'utf-8')
    assert result_bytes.result     == bytearray('test', 'utf-8')
    assert result_bytestr.result   == bytearray('test', 'utf-8')

def test_byte_regex():

    parser = byte.regex(b'[A-Z]+')

    status_bytearray = Status(bytearray('TEST', 'utf-8'))
    status_bytes     = Status(bytes('TEST', 'utf-8'))
    status_bytestr   = Status(b'TEST')

    result_bytearray = parser.run(status_bytearray)
    result_bytes     = parser.run(status_bytes)
    result_bytestr   = parser.run(status_bytestr)

    assert type(result_bytes.result) == bytes

    assert result_bytearray.result == bytes('TEST', 'utf-8')
    assert result_bytes.result     == bytes('TEST', 'utf-8')
    assert result_bytestr.result   == bytes('TEST', 'utf-8')

def test_byte_newl():

    parser = byte.newl()
    status = Status(b'\n')
    result = parser.run(status)

    assert result.result == b'\n'

    parser = zjadacz.sequenceOf(
        byte.regex(b'[A-Z]+'),
        byte.newl(),
        byte.regex(b'[a-z]+'),
        byte.newl(),
    )
    status = Status(b'HELLO\nworld\n')
    result = parser.run(status)

    assert result.result == [b'HELLO', b'\n', b'world', b'\n']

def test_byte_unumber():

    parser = byte.unumber()
    status = Status(b'2137')
    result = parser.run(status)

    assert result.result == 2137

def test_byte_snumber():

    parser = byte.snumber()
    status = Status(b'2137')
    result = parser.run(status)

    assert result.result == 2137

    status = Status(b'+69420')
    result = parser.run(status)

    assert result.result == 69420

    status = Status(b'-13')
    result = parser.run(status)

    assert result.result == -13