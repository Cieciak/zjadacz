from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Self
import re

class Types(Enum):
    STRING = 'String'
    DIGITS = 'Digits'
    EOF    = 'End Of File'

@dataclass
class Result:
    '''Actual result of parsing data'''
    type: Types = None
    value: Any  = None

    def __repr__(self) -> str:
        type_s  = f'{self.type.value}'
        value_s = f'[{self.value}]' if self.value else ''
        return f'{type_s}{value_s}'

@dataclass
class ParserStatus:
    '''Return value of all transformer functions'''
    isFailure: bool = False
    error: str = None

    data: str = ''

    offset: int = 0
    result: Result = None

    @property
    def head(self):
        '''Data after offset'''
        return self.data[self.offset:]
    
    def update(self, **overwrites: dict) -> Self:
        '''Create updated copy of status and return'''
        fields = self.__dict__.copy()
        for key, value in overwrites.items(): fields[key] = value
        return ParserStatus(**fields)
    
    def __repr__(self) -> str:
        status = '🟥' if self.isFailure else '🟩'
        payload = self.error if self.isFailure else self.result
        return f'{status} {payload}'

class Parser:
    def __init__(self, transformer: Callable[[ParserStatus], ParserStatus]):
        self.transformer = transformer

    def run(self, data: str) -> ParserStatus:
        initial = ParserStatus(
            isFailure = False,
            error = None,

            data = data,

            offset = 0,
            result = None,
        )
        return self.transformer(initial)
    
    def map(self, function: Callable) -> Self:
        def wrapper(status: ParserStatus) -> ParserStatus:
            current = self.transformer(status)
            return current.update(result = function(current.result))
        return Parser(wrapper)
    
    def chain(self, function: Callable[[ParserStatus], Self]) -> Self:
        def wrapper(status: ParserStatus) -> ParserStatus:
            current = self.transformer(status)

            nextParser = function(current)
            return nextParser.transformer(current)
        return Parser(wrapper)
    
def string(pattern: str) -> Parser:
    def transformer(status: ParserStatus) -> ParserStatus:
        flag = status.head.startswith(pattern)

        if flag:
            # Found the the patter in data
            return status.update(
                result = Result(value = pattern, type = Types.STRING),
                offset = len(pattern) + status.offset,
            )
        elif status.head == '':
            # End of file reached
            return status.update(
                isFailure = True,
                error = 'EOF in unexpected place'
            )
        else:
            # No match found
            return status.update(
                isFailure = True,
                error = f'Tried to match \"{pattern}\", but got \"{status.head[:len(pattern)]}\"'
            )
    return Parser(transformer)

def letters() -> Parser:
    def transformer(status: ParserStatus) -> ParserStatus:
        check = re.compile(r'^[a-zA-Z]+').match(status.head)
        if check:
            return status.update(
                result = Result(value = check.group(), type = Types.STRING),
                offset = status.offset + check.end()
            )
        elif status.head == '':
            return status.update(
                isFailure = True,
                error = 'EOF in unexpected place'
            )
        else:
            return status.update(
                isFailure = True,
                error = f'No letters on \"{status.head[:10]}\"'
            )
    return Parser(transformer)

def eof() -> Parser:
    def transformer(status: ParserStatus) -> ParserStatus:
        if status.head == '':
            return status.update(
                result = Result(value = None, type = Types.EOF)
            )
        else:
            return status.update(
                isFailure = True,
                error = 'Buffer not empty'
            )
    return Parser(transformer)


def digits() -> Parser:
    def transformer(status: ParserStatus) -> ParserStatus:
        check = re.compile(r'^[0-9]+').match(status.head)
        if check:
            return status.update(
                result = Result(value = check.group(), type = Types.DIGITS),
                offset = status.offset + check.end()
            )
        elif status.head == '':
            return status.update(
                isFailure = True,
                error = 'EOF in unexpected place'
            )
        else:
            return status.update(
                isFailure = True,
                error = f'No digits on \"{status.head[:10]}\"'
            )
    return Parser(transformer)  

def sequenceOf(*pattern: Parser) -> Parser:
    def transformer(status: ParserStatus) -> ParserStatus:
        result = []
        current = status

        for p in pattern:
            current = p.transformer(current)
            if current.isFailure: return current
            result.append(current.result)

        return current.update(result = result)
    return Parser(transformer)

def choice(*options: Parser) -> Parser:
    def transformer(status: ParserStatus) -> ParserStatus:
        for p in options:
            result = p.transformer(status)
            if result.isFailure: continue
            return result
        return result
    return Parser(transformer)

def many(pattern: Parser) -> Parser:
    def transformer(status: ParserStatus) -> ParserStatus:
        gathered = []
        current = status
        while True:
            current = pattern.transformer(current)
            if current.isFailure:
                return current.update(isFailure = False, error = None, result = gathered, offset = current.offset)
            
            gathered.append(current.result)
    return Parser(transformer)

def manyStrict(pattern: Parser) -> Parser:
    def transformer(status: ParserStatus) -> ParserStatus:
        gathered = []
        current = status
        while True:
            current = pattern.transformer(current)
            if current.isFailure and gathered:
                return current.update(isFailure = False, error = None, result = gathered, offset = current.offset)
            elif current.isFailure: 
                return status.update(isFailure = True, error = f'Couldn\'t match any')
            
            gathered.append(current.result)
    return Parser(transformer)

def between(left: Parser, right: Parser) -> Callable[[Parser], Parser]:
    def operator(content: Parser) -> Parser:
        return sequenceOf(left, content, right).map(lambda result: result[1])
    return operator

def separatedBy(separator: Parser) -> Callable[[Parser], Parser]:
    def operator(content: Parser) -> Parser:
        def transformer(status: ParserStatus) -> ParserStatus:
            gathered = []
            next = status

            while True:
                temp = content.transformer(next)
                if temp.isFailure: break

                gathered.append(temp.result)
                next = temp

                temp = separator.transformer(next)
                if temp.isFailure: break

                next = temp

            return next.update(isFailure = False, error = None, result = gathered)
        return Parser(transformer)
    return operator

def lazy(thunk: Callable[[], Parser]) -> Parser:
    def transformer(status: ParserStatus) -> ParserStatus:
        return thunk().transformer(status)
    return Parser(transformer)


if __name__ == '__main__':
    p = sequenceOf(
        digits(),
        many(
            choice(
                string(' '),
                letters(),
            ),
        ),
        digits(),
        eof(),
    )

    # "string:helloe"
    # "integer:3437"
    # "dice:3d36"

    test = '1d30'
    q = p.run(test)
    print(q)

    test = 'dd30'
    q = p.run(test)
    print(q)

    test = '2 hejo lol30'
    q = p.run(test)
    print(q)

    wrapper = between(string('"'), string('"'))

    strin = sequenceOf(letters(), string(":")).map(lambda result: result[0]).chain(lambda r: letters() if r.result.value == 'string' else digits())


    p = wrapper(strin)
    
    commasep = separatedBy(string(","))

    listed = commasep(digits())
    wrapper = between(string('['), string(']'))
    listed = wrapper(listed)
    test = '[4454534,67,4534,5465,34556,4545]'
    q = listed.run(test)
    print(q)

    test = '"digits:3456"'
    q = p.run(test)
    print(q)

    test = '"string:helloe"'
    q = p.run(test)
    print(q)

    l = lazy(lambda: sequenceOf(letters(), digits()))
    test = 'rgergerg45456'
    q = l.run(test)
    print(q)

    betweenSquare = between(string('['), string(']'))
    separatedComma = separatedBy(string(','))

    value = lazy(lambda: choice(digits(), arrayParser))

    arrayParser = betweenSquare(separatedComma(value))

    test = '[1,[2,[3],4],5]'
    q = arrayParser.run(test)
    print(q)