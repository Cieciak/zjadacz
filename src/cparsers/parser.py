from .status import Status
from .error import ParserError

from copy import copy

class Parser:

    def __init__(self, transformer):
        self.transformer = transformer

    def run(self, initial: Status) -> Status:
        return self.transformer(initial)

    @classmethod
    def Simplex(cls, target):
        def check(status: Status) -> Status:
            if len(status.head) == 0: return ParserError("Unexpected EOF")
            flag = status.head[0] == target
            if flag: return Status.result(status.head[0], status=status, increment=1)
            return ParserError(f"Cannot match [{status.head[0]}] with [{target}]")
        return cls(check)

    @classmethod
    def SequenceOf(cls, *parsers):
        def check(status: Status) -> Status:
            result = []
            current = status
            for pattern in parsers:
                current = pattern.transformer(current)
                if isinstance(current, ParserError):
                    return ParserError.propagate("Cannot get sequence", current)
                result.append(current.result)
            # Ater loop the offset is at correct location, so we can just take the last loop result
            return Status.result(result, status=current, increment=0)
        return cls(check)

    @classmethod
    def ChoiceOf(cls, *parsers):
        def check(status: Status) -> Status:
            cstatus = copy(status)
            for pattern in parsers:
                result = pattern.transformer(cstatus)
                if isinstance(result, ParserError): continue
                return result
            # No match, return trace from the last attempt
            return ParserError.propagate("All the path for choice failed", result)
        return cls(check)

    @classmethod
    def Many(cls, pattern, *, strict: bool = False):
        def check(status: Status) -> Status:
            gathered = []
            current = status
            # TODO: Safeguard this
            while True:
                result = pattern.transformer(current)
                if isinstance(result, ParserError): break
                gathered.append(result.result)
                current = result
            # Strict mode disallows empty match
            if strict and (len(gathered) == 0): return ParserError.propagate("Matching many in strict mode failed", result)
            print("tried to return ")
            return Status.result(gathered, status=current, increment=0)
        return cls(check)

    @classmethod
    def Lazy(cls, thunk):
        def transformer(status: Status) -> Status:
            return thunk().transformer(status)
        return cls(transformer)

    def map(self, function):
        def wrapper(status: Status) -> Status:
            current = self.transformer(status)
            if isinstance(current, ParserError): return current
            return Status.result(function(current), status=status)
        return Parser(wrapper)

    def chain(self, function):
        def wrapper(status: Status) -> Status:
            current = self.transformer(status)
            if isinstance(current, ParserError): return current
            nextParser = function(current)
            return nextParser.transformer(current)
        return Parser(wrapper)
