from typing import Self
from copy import copy

class Status:

    def __init__(self, data, offset: int = 0, context: dict = None):
        self.data = data
        self.offset = offset
        self.context = dict() if context is None else context
        self.result = None

    def __repr__(self):
        return f'{self.result}'

    @property
    def head(self):
        return self.data[self.offset:]

    @property
    def copy(self) -> Self:
        return copy(self)

    def chainResult(self, result, increment: int):
        # Create copy to avoid passing by reference
        new = copy(self)
        new.offset += increment
        new.result = result

        return new