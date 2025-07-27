import zjadacz
import zjadacz.string

import pprint

identifier = zjadacz.string.regex("[A-Z]+")
walrus = zjadacz.string.word("::=")
modifier = zjadacz.choiceOf(
    zjadacz.string.word("*"), # Many modifier
    zjadacz.string.word("+"), # At least one modifier
    zjadacz.string.word("?"), # Optional modifier
    zjadacz.string.word(""),
)
endl = zjadacz.sequenceOf(
    zjadacz.string.word(";"),
    zjadacz.optional(
        zjadacz.many(
            zjadacz.string.word('\n'),
            strict=True,
        )
    )
)

scpSep = zjadacz.separated(zjadacz.string.word(" "))

def build_parser1():
    sequence = zjadacz.sequenceOf(
        zjadacz.string.word("("),
        zjadacz.lazy(lambda: expr),
        zjadacz.many(
            zjadacz.sequenceOf(
                zjadacz.string.word(" "),
                zjadacz.lazy(lambda: expr),
            ).map(lambda s: s.result[1::2])
        ).map(lambda s: [item[0] for item in s.result]),
        zjadacz.string.word(")"),
    ).map(lambda s: {"sequence": [s.result[1], *s.result[2]]})


    expr = zjadacz.sequenceOf(
        zjadacz.choiceOf(
            sequence,
            identifier,
        ),
        zjadacz.choiceOf(
            zjadacz.word('*'),
            zjadacz.word(''),
        ),
    )

    definition = zjadacz.sequenceOf(
        identifier,
        walrus,
        expr,
        zjadacz.string.word(";"),
    )

    parser = zjadacz.many(
        definition,
    )

    return parser

def build_parser():

    sequence = zjadacz.sequenceOf(
        zjadacz.string.word("("),
        scpSep(zjadacz.lazy(lambda: expr)),
        zjadacz.string.word(")")
    ).map(
        lambda s: {
            'sequence': s.result[1],
        }
    )

    choice = zjadacz.sequenceOf(
        zjadacz.string.word("["),
        scpSep(zjadacz.lazy(lambda: expr)),
        zjadacz.string.word("]")
    ).map(
        lambda s: {
            'choice': s.result[1],
        }
    )

    expr = zjadacz.sequenceOf(
        zjadacz.choiceOf(
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

    definition = zjadacz.sequenceOf(
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

    parser = zjadacz.many(
        definition
    )

    return parser



def load_file(path: str) -> str:

    with open(path, 'r') as file:
        data = file.read()

    return data

def run_file(path: str, parser: zjadacz.Parser) -> str:
    print("\n" + "#" * 80 + "\n" + "#" * 80 + f"\nRunning file: {path}\n")

    data = load_file(path)
    print(f"File data:\n{data}\n")

    return parser.run(zjadacz.Status(data))

def print_result(result: zjadacz.Status | zjadacz.ParserError):
    match result:
        case zjadacz.Status():
            pprint.pprint(result.result)
        case zjadacz.ParserError():
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
            body = zjadacz.sequenceOf(*p)
        elif 'choice' in expr.keys():
            p = [
                compile_ast(inner, glob) for inner in expr['choice']
            ]
            body = zjadacz.choiceOf(*p)

    match ast['mod']:
        case '*':
            return zjadacz.many(body)
        case '+':
            return zjadacz.many(body, strict=True)
        case '?':
            return zjadacz.optional(body)
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
        'HELLO': zjadacz.string.word('Hello'),
        'WELCOME': zjadacz.string.word('Welcome'),
        'WORLD': zjadacz.string.word('World'),
        'NUMBER': zjadacz.string.sint(),

        'SPC': zjadacz.string.word(' '),
    }

    for definition in result.result:
        name, parser = compile_def(definition, glob)

        glob[name] = parser

        pprint.pprint(glob)

    r = glob['TARGET'].run(zjadacz.Status('Hello World 334 565 '))
    print_result(r)