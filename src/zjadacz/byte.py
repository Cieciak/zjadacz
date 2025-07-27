import re

from .status import Status
from .parser import Parser
from .error  import ParserError

def word(datain: bytes) -> Parser:
    data = bytes(datain)

    def transformer(status: Status) -> Status:
        flag = bytes(status.head).startswith(data)

        if flag: return status.chainResult(data, increment=len(data))
        return ParserError(f'Cannot match {data} with {status.head[:len(data)]}')
    return Parser(transformer)

def regex(patternin: bytes) -> Parser:
    pattern = re.compile(bytes(patternin))

    def transformer(status: Status) -> Status:
        matched = pattern.match(bytes(status.head))

        if matched:
            group = matched.group()
            return status.chainResult(group, increment=len(group))
        return ParserError(f'Cannot match {pattern} with {status.head[:20]}')
    return Parser(transformer)

def newl() -> Parser:
    def transformer(status: Status) -> Status:
        flag = bytes(status.head).startswith(b'\n')

        if flag: return status.chainResult(b'\n', increment=1)
        return ParserError(f'Cannot get new line')
    return Parser(transformer)

def unumber() -> Parser: return regex(br'[1-9][0-9]*').map(lambda s: int(s.result))

def snumber() -> Parser: return regex(br'[\-\+]?[1-9][0-9]*').map(lambda s: int(s.result))