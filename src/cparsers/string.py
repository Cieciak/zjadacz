import re
from typing import Self

from .status import Status
from .error  import ParserError
from .parser import Parser
    
def word(text: str) -> Parser:
    def check(status: Status) -> Status:
        flag = str(status.head).startswith(text)
        if flag: return status.chainResult(text, increment=len(text))
        return ParserError(f'Cannot match {text} with {status.head[:len(text)]}')
    return Parser(check)

def regex(pattern: str) -> Parser: 
    def check(status: Status) -> Status:
        matched = re.compile(pattern).match(str(status.head))
        if matched:
            group = matched.group()
            return status.chainResult(group, increment=len(group))
        return ParserError(f'Cannot match {regex} with {status.head[:20]}')
    return Parser(check)

def uint() -> Parser: return regex(r'[1-9][0-9]*').map(lambda s: int(s.result))

def sint() -> Parser: return regex(r'[\-\+]?[1-9][0-9]*').map(lambda s: int(s.result))