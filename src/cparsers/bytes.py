from .parser import Parser
from .status import Status
from .error import ParserError

def byte() -> Parser:
    def check(status: Status) -> Status:
        content = bytes(status.head)

        if len(content) == 0: return ParserError('Unexpected EOD')
        return status.chainResult(content[0], increment=1)
    return Parser(check)

def word() -> Parser:
    def check(status: Status) -> Status:
        content = bytes(status.head)

        if len(content) < 2: return ParserError('Not enough data')
        return status.chainResult(content[0:2], increment=2)
    return Parser(check)

def dword() -> Parser:
    def check(status: Status) -> Status:
        content = bytes(status.head)

        if len(content) < 4: return ParserError('Not enough data')
        return status.chainResult(content[0:4], increment=2)
    return Parser(check)

def qword() -> Parser:
    def check(status: Status) -> Status:
        content = bytes(status.head)

        if len(content) < 8: return ParserError('Not enough data')
        return status.chainResult(content[0:8], increment=2)
    return Parser(check)

def uint8(dir: str = None) -> Parser:
    return byte().map(lambda s: __uint_from_bytes([s.result, ], 1, True))

def uint16(dir: str) -> Parser:
    match dir.lower():
        case 'msb': flag = True
        case 'lsb': flag = False
        case _: ValueError('dir must be \'msb\' or \'lsb\'')
    return word().map(lambda s: __uint_from_bytes(s.result, 2, flag))

def uint32(dir: str) -> Parser:
    match dir.lower():
        case 'msb': flag = True
        case 'lsb': flag = False
        case _: ValueError('dir must be \'msb\' or \'lsb\'')
    return dword().map(lambda s: __uint_from_bytes(s.result, 4, flag))

def uint64(dir: str) -> Parser:
    match dir.lower():
        case 'msb': flag = True
        case 'lsb': flag = False
        case _: ValueError('dir must be \'msb\' or \'lsb\'')
    return qword().map(lambda s: __uint_from_bytes(s.result, 8, flag))

def __uint_from_bytes(array: bytes, length: int, msb: bool):
    dire = 1 if msb else -1 
    data = array[0:length]

    value = 0
    for b in data[::dire]:
        value = 256 * value + int(b)

    return value