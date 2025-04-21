import cparsers
import cparsers.string

import pprint

identifier = cparsers.string.regex("[A-Z]+")
walrus = cparsers.string.word("::=")
modifier = cparsers.choiceOf(
    cparsers.string.word("*"), # Many modifier
    cparsers.string.word("+"), # At least one modifier
    cparsers.string.word("?"), # Optional modifier
    cparsers.string.word(""),
)
endl = cparsers.sequenceOf(
    cparsers.string.word(";"),
    cparsers.optional(
        cparsers.string.word('\n'),
    )
)

scpSep = cparsers.separated(cparsers.string.word(" "))

def build_parser1():
    sequence = cparsers.sequenceOf(
        cparsers.string.word("("),
        cparsers.lazy(lambda: expr),
        cparsers.many(
            cparsers.sequenceOf(
                cparsers.string.word(" "),
                cparsers.lazy(lambda: expr),
            ).map(lambda s: s.result[1::2])
        ).map(lambda s: [item[0] for item in s.result]),
        cparsers.string.word(")"),
    ).map(lambda s: {"sequence": [s.result[1], *s.result[2]]})


    expr = cparsers.sequenceOf(
        cparsers.choiceOf(
            sequence,
            identifier,
        ),
        cparsers.choiceOf(
            cparsers.word('*'),
            cparsers.word(''),
        ),
    )

    definition = cparsers.sequenceOf(
        identifier,
        walrus,
        expr,
        cparsers.string.word(";"),
    )

    parser = cparsers.many(
        definition,
    )

    return parser

def build_parser():

    sequence = cparsers.sequenceOf(
        cparsers.string.word("("),
        scpSep(cparsers.lazy(lambda: expr)),
        cparsers.string.word(")")
    ).map(
        lambda s: {
            'sequence': s.result[1],
        }
    )

    choice = cparsers.sequenceOf(
        cparsers.string.word("["),
        scpSep(cparsers.lazy(lambda: expr)),
        cparsers.string.word("]")
    ).map(
        lambda s: {
            'choice': s.result[1],
        }
    )

    expr = cparsers.sequenceOf(
        cparsers.choiceOf(
            sequence,
            choice,
            identifier,
        ),
        modifier,
    ).map(
        lambda s: {
            'expr': s.result[0],
            'mod': s.result[1]
        }
    )

    definition = cparsers.sequenceOf(
        identifier,
        walrus,
        expr,
        endl,
    ).map(
        lambda s: {
            'name': s.result[0],
            'body': s.result[2],
        }
    )

    parser = cparsers.many(
        definition
    )

    return parser



def load_file(path: str) -> str:

    with open(path, 'r') as file:
        data = file.read()

    return data

def run_file(path: str, parser: cparsers.Parser) -> str:
    print("\n" + "#" * 80 + "\n" + "#" * 80 + f"\nRunning file: {path}\n")

    data = load_file(path)
    print(f"File data:\n{data}\n")

    return parser.run(cparsers.Status(data))

def print_result(result: cparsers.Status | cparsers.ParserError):
    match result:
        case cparsers.Status():
            pprint.pprint(result.result)
        case cparsers.ParserError():
            print(result)

if __name__ == '__main__':
    

    path = "examples/rozwik/samples/01.roz"
    root = build_parser()
    result = run_file(path, root)
    print_result(result)

    path = "examples/rozwik/samples/02.roz"
    root = build_parser()
    result = run_file(path, root)
    print_result(result)

    path = "examples/rozwik/samples/03.roz"
    root = build_parser()
    result = run_file(path, root)
    print_result(result)