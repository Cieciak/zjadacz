import re

from .status import Status
from .error  import ParserError
from .parser import Parser

class StringParser(Parser):

    @classmethod
    def word(cls, text: str):
        def check(s: Status) -> Status:
            flag = str(s.head).startswith(text)

            if flag: return s.chainResult(text, increment=len(text))
            return ParserError(f'Cannot match {text} with {s.head[:len(text)]}')
        return cls(check)
    
    @classmethod
    def regex(cls, regex: str):
        def check(s: Status) -> Status:
            matched = re.compile(regex).match(str(s.head))

            if matched: 
                group = matched.group()
                print(f'{group=}, {len(group)=}')

                r = s.chainResult(group, increment=len(group))
                print(f'{r.offset=}')
                return r
            return ParserError(f'Cannot match {regex} with {s.head[:20]}')
        return cls(check)
    
def word(text: str): return StringParser.word(text)

def regex(pattern: str): return StringParser.regex(pattern)

def uint(): return StringParser.regex(r'[1-9][0-9]*').map(lambda s: int(s.result))

def sint(): return StringParser.regex(r'[\-\+]?[1-9][0-9]*').map(lambda s: int(s.result))