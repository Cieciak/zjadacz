from typing import Self

class ParserError:

    def __init__(self, reason: str):
        self.reason: str = reason
        self.trace: list[ParserError] = []

    def __repr__(self) -> str:
        head = f"Parser Error: {self.reason}"
        spcn = "\n    " if self.trace else ""
        trac = "\n    ".join([err.reason for err in self.trace])
        return head + spcn + trac

    @classmethod
    def propagate(cls, reason, source) -> Self:
        # Make error from local reasocn of failure
        err = cls(reason)

        # Add more context to error
        err.trace.append(source)
        err.trace.extend(source.trace)
        return err
