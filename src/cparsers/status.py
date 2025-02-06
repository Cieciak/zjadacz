from copy import copy

class Status:

    def __init__(self, data, offset: int = 0, context: dict = None):
        self.data = data
        self.offset = offset
        self.context = dict() if context is None else context
        self.result = None

    def __repr__(self):
        return f'{self.result}'

    @classmethod
    def result(cls, result, data = None, offset: int = 0, context: dict = None, *, status = None, increment = 0):
        # Can pass both raw data, or base result on previous status
        if status is None:
            if data is None: raise ValueError("Data cammot be None")
            obj = cls(data, offset + increment, context)
        else:
            obj = status
            obj.offset += increment
        obj.result = result
        return obj

    @property
    def head(self):
        # Get data after offset
        return self.data[self.offset:]

    def chainResult(self, result, increment: int):
        # Create copy to avoid passing by reference
        new = copy(self)
        new.offset += increment
        new.result = result

        return new