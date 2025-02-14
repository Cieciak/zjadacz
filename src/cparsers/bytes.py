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