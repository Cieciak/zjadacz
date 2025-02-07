from .status import Status
from .error import ParserError
from .parser import Parser

from typing import Any

def simplex(target: Any):
    '''Will match ony one static object'''
    def check(status: Status) -> Status:
        if len(status.head) == 0: return ParserError('Unexpected end of file')

        if status.head[0] == target:
            return status.chainResult(status.head[0], increment=1)
        return ParserError(f'Can\'t match [{target}] to [{status.head[0]}]')
    return Parser(check)

def sequenceOf(*parsers: Parser):
    def check(status: Status) -> Status:
        result: list[Any] = list()
        current = status.copy

        for pattern in parsers:
            current = pattern.transformer(current)
            if isinstance(current, ParserError):
                return ParserError.propagate("Can't get sequence", current)
            result.append(current.result)

        # After loop the offset is at correct location, so we can just take the last loop result
        return current.chainResult(result, increment=0)
    return Parser(check)

def choiceOf(*parsers: Parser):
    def check(status: Status) -> Status:
        current = status.copy

        for pattern in parsers:
            result = pattern.transformer(current)
            if isinstance(result, ParserError): continue
            return result
        # No match, return trace from last attempt, TODO: Decide how this should be handled
        return ParserError.propagate("All the path for choice failed", result)
    return Parser(check)

def many(pattern, *, strict: bool = False): return Parser.Many(pattern, strict=strict)

def lazy(thunk): return Parser.Lazy(thunk)



def between(left: Parser, right: Parser):
    def operator(content: Parser):
        return sequenceOf(left, content, right).map(
            lambda status: status.result[1]
        )
    return operator

def separated(sep: Parser):
    def operator(content: Parser):
        def transformer(status: Status):
            gathered = []
            next = status
            while True:
                temp = content.transformer(next)
                if isinstance(temp, ParserError): break
                gathered.append(temp.result)
                next = temp
                temp = sep.transformer(next)
                if isinstance(temp, ParserError): break
                next = temp
            return next.chainResult(gathered, increment=0)
        return Parser(transformer)
    return operator
