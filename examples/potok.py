from zjadacz import *
from zjadacz import string
from zjadacz import byte

def listToDict(data):
    output: dict = {}
    for tag in data:
        output = {**output, **tag}

    return output

segment_name_parser = sequenceOf(
    string.word('-'),
    string.regex('[A-Z]+'),
    string.word('-\n'),
).map(
    lambda s: s.result[1]
)

begin_segment = sequenceOf(
    string.regex('[A-Z]+'),
    string.word('\n'),
    string.regex('[0-9]+\\.[0-9]+'),
    string.word('\n'),
    string.regex('[A-Z]+'),
    string.word('\n'),
).map(
    lambda s: (s.result[0], s.result[2], s.result[4])
)

tag_line_praser = sequenceOf(
    string.regex('[A-Za-z]+'),
    string.word(': '),
    string.regex('[A-Za-z0-9]+'),
    string.word('\n'),
).map(
    lambda s: {s.result[0]: s.result[2]}
)

head_segment = many(
    tag_line_praser,
).map(
    lambda s: listToDict(s.result)
)

body_segment_parser = choiceOf(
    string.regex('.*?(?=-[A-Z]+-)'),
    string.regex('.*'),
)

segment_parser = segment_name_parser.match(
    {
        'BEGIN': begin_segment,
        'HEAD': head_segment,
        'BODY': body_segment_parser,
    }
)

potok_parser = sequenceOf(
    segment_parser,
    segment_parser,
    segment_parser,
)

if __name__ == '__main__':
    potok_msg = '''-BEGIN-
POTOK
0.1
GET
-HEAD-
Target: there
Origin: here
Location: home
-BODY-
rawdata'''



    r = potok_parser.run(Status(potok_msg))

    print(r)

    potok_msg_bytes = b'test'

    byte_parser = byte.word(b'test')

    result = byte_parser.run(Status(potok_msg_bytes))

    print(result)
