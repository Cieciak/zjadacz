import cparsers
import cparsers.string

import pprint
import sys

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
regex = cparsers.string.regex('/(?<=/)(.*?)(?=/)/').map(lambda s: {'regex': s.result})
scpSep = cparsers.separated(cparsers.string.word(" "))

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
            regex,
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
        elif 'regex' in expr.keys():
            body = cparsers.string.regex(expr['regex'])

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
    root = build_parser()
    path = sys.argv[1]

    try: result = run_file(path, root)
    except FileNotFoundError:
        print(f"Can\'t find \"{path}\" file!")
        quit()

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

    r = glob['TARGET'].run(cparsers.Status('Hello World 334 565 '))
    print_result(r)