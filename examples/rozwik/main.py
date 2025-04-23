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
        cparsers.many(
            cparsers.string.word('\n'),
            strict=True,
        )
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

def compile_def(ast: dict, glob):
    name = ast['name']
    body = compile_ast(ast['body'], glob)

    return name, body

def compile_ast(ast: dict, glob):
    if type(ast['expr']) == str:
        body = glob[ast['expr']]
    elif type(ast['expr']) == dict:
        expr = ast['expr']
        if 'sequence' in expr.keys():
            p = [
                compile_ast(inner, glob) for inner in expr['sequence']
            ]
            body = cparsers.sequenceOf(*p)
        elif 'choice' in expr.keys():
            p = [
                compile_ast(inner, glob) for inner in expr['choice']
            ]
            body = cparsers.choiceOf(*p)

    match ast['mod']:
        case '*':
            return cparsers.many(body)
        case '+':
            return cparsers.many(body, strict=True)
        case '?':
            return cparsers.optional(body)
        case '':
            return body


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

    path = "examples/rozwik/samples/05.roz"
    root = build_parser()
    result = run_file(path, root)
    print_result(result)

    glob = {
        'HELLO': cparsers.string.word('Hello'),
        'WELCOME': cparsers.string.word('Welcome'),
        'WORLD': cparsers.string.word('World'),
        'NUMBER': cparsers.string.sint(),

        'SPC': cparsers.string.word(' '),
    }

    for definition in result.result:
        name, parser = compile_def(definition, glob)

        glob[name] = parser

        pprint.pprint(glob)

    r = glob['TARGET'].run(cparsers.Status('Hello World 334 565 '))
    print_result(r)