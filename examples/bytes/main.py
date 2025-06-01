import cparsers
from typing import Callable
from cparsers import Status, ParserError, Parser

from pprint import pprint

def addContext(s: Status) -> Status:
    s.context['offset'] = s.result['data-offset']
    return s

def getWord() -> Parser:
    def consumer(s: Status) -> Status:
        if len(s.head) == 0: return ParserError('End Of Data')

        value = s.head[1] + 256 * s.head[0]
        
        return Status.chainResult(s, value, increment=2)
    return Parser(consumer)

def getByte() -> Parser:
    def consumer(s: Status) -> Status:
        if len(s.head) == 0: return ParserError('End Of Data')

        value = s.head[0]
        
        return Status.chainResult(s, value, increment=1)
    return Parser(consumer)


getDoubleword = cparsers.sequenceOf(
    getWord(),
    getWord(),
).map(lambda s: s.result[1] + 256 * s.result[0])

def getOpts() -> Parser:
    def consumer(s: Status) -> Status:
        data_len = s.context['offset'] - 5
        if data_len == 0: return s.chainResult(None, increment=0)
        if len(s.head) == 0: return ParserError('End Of Data')

        result = []
        status = s
        for _ in range(data_len):
            status = getDoubleword.transformer(status)
            if isinstance(status, ParserError): return ParserError.propagate('Can\'t get enogh repetitions', status)
            result.append(status.result)

        return status.chainResult(result, increment=0)
    return Parser(consumer)




        
tcp_head = cparsers.sequenceOf(
    getWord(),
    getWord(),
    getDoubleword,
    getDoubleword,
    getByte(),
    getByte(),
    getWord(),
    getWord(),
    getWord(),
).map(
    lambda s: {
        'src-port': s.result[0],
        'dst-port': s.result[1],
        'seq-number': s.result[2],
        'ack-number': s.result[3],
        'data-offset': s.result[4] >> 4,
        'flags': s.result[5],
        'window': s.result[6],
        'checksum': s.result[7],
        'urgen-ptr': s.result[8],
    }
).chain(lambda s: Parser(addContext))

tcp = cparsers.sequenceOf(
    tcp_head,
    getOpts(),
)

if __name__ == '__main__':

    status = cparsers.Status(b'\x1f\x90\x00\x60\x00\x00\x00\x01\x00\x00\x00\x00\x60\x02\x20\x00\x00\x00\x00\x01\x01\x01\x01\x01')

    root = tcp

    result = root.run(status)

    print(status.data)
    pprint(result.result)
    pprint(result.context)