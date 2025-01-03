class ParserError:

    def __init__(self, reason: str):
        self.reason = reason
        self.trace = []

    def __repr__(self):
        head = f"Parser Error: {self.reason}"
        spcn = "\n    " if self.trace else ""
        trac = "\n    ".join([err.reason for err in self.trace])
        return head + spcn + trac

    @classmethod
    def propagate(cls, reason, source):
        # Make error from local reasocn of failure
        err = cls(reason)

        # Add more context to error
        err.trace.append(source)
        err.trace.extend(source.trace)
        return err
