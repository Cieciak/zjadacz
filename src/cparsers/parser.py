from typing import Callable, Any, Self

from .status import Status
from .error import ParserError

class Parser:

    def __init__(self, transformer: Callable[[Status], Status]):
        self.transformer: Callable[[Status], Status] = transformer

    def run(self, initial: Status) -> Status:
        return self.transformer(initial)

    def map(self, function: Callable[[Status], Any]) -> Self:
        def wrapper(status: Status) -> Status:
            current = self.transformer(status)
            if isinstance(current, ParserError): return current
            return current.chainResult(function(current), increment=0)
        return Parser(wrapper)

    def chain(self, function: Callable[[Status], Self]) -> Self:
        def wrapper(status: Status) -> Status:
            current = self.transformer(status)
            if isinstance(current, ParserError): return current
            nextParser = function(current)
            return nextParser.transformer(current)
        return Parser(wrapper)
        
    def reassign(self, parser: Self):
        self.transformer = parser.transformer