import cparsers
import cparsers.string

from typing import Callable, Any
import pprint
import sys

import loader


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


def build_parser() -> cparsers.Parser:

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


    decorator = cparsers.sequenceOf(
        cparsers.string.word("@"),
        cparsers.string.regex("[a-z]+"),
        cparsers.string.word('\n'),
    ).map(lambda s: {'decorator': s.result[1]})

    definition = cparsers.sequenceOf(
        cparsers.optional(decorator).map(lambda s: s.result if s.result else {}),
        identifier,
        walrus,
        expr,
        endl,
    ).map(
        lambda s: {
            'name': s.result[1],
            'body': s.result[3],
            'deco': s.result[0] if 'decorator' in s.result[0] else None,
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

def compile_def(ast: dict, glob, maps: dict[str, Callable[[cparsers.Status], Any]]):
    name = ast['name']
    body = compile_ast(ast['body'], glob)

    deco = ast['deco']
    if deco:
        wrapper = maps[deco['decorator']]
        body = body.map(wrapper)

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


def compileDefinitionToPython(ast: dict, *, parsers = {}, maps = {}):
    name = ast['name']
    body = ast['body']
    deco = ast['deco']

    body = compileToPython(body)

    if deco:
        body += '.map(ext_m[\'' + deco['decorator'] + '\'])'

    return f'{name}={body}'


def compileToPython(ast: dict):
    if type(ast['expr']) == str:
        body = ast['expr']
    elif type(ast['expr']) == dict:
        expr = ast['expr']
        if 'sequence' in expr.keys():
            p = [
                compileToPython(inner) for inner in expr['sequence']
            ]
            body = 'cparsers.sequenceOf(' + ', '.join(p) + ')' 
        elif 'choice' in expr.keys():
            p = [
                compileToPython(inner) for inner in expr['choice']
            ]
            body = 'cparsers.choiceOf(' + ', '.join(p) + ')'
        elif 'regex' in expr.keys():
            body = 'cparsers.string.regex(r\"' + expr['regex'][1:-1] + '\")'

    match ast['mod']:
        case '*':
            return f'cparsers.many({body})'
        case '+':
            return f'cparsers.many({body}, strict=True)'
        case '':
            return f'{body}'

if __name__ == '__main__':
    root = build_parser()
    path = sys.argv[1]
    ext_p, ext_m = loader.importExtension('examples/rozwik/ext/01.py')

    body = '''
import cparsers
import cparsers.string

import sys
import loader

ext_p, ext_m = loader.importExtension('examples/rozwik/ext/01.py')

def build_parser():'''
    
    try: result = run_file(path, root)
    except FileNotFoundError:
        print(f'Can\'t find \"{path}\" file!')
        quit()

    for definition in result.result:
        print('\n' + '#' * 80)
        print(definition)
        body += '\n    ' + compileDefinitionToPython(definition, parsers=ext_p, maps=ext_m)

    body += '\n    return TARGET\n'

    body += '''
if __name__ == '__main__':
    root = build_parser()
    data = sys.argv[1]

    s = cparsers.Status(data)
    r = root.run(s)
    print(r)
'''

    with open('examples/rozwik/out.py', 'w') as file:
        file.write(body)


# if __name__ == '__main__':
#     root = build_parser()
#     path = sys.argv[1]

#     try: result = run_file(path, root)
#     except FileNotFoundError:
#         print(f"Can\'t find \"{path}\" file!")
#         quit()

#     print_result(result)

#     glob = {
#         'HELLO': cparsers.string.word('Hello'),
#         'WELCOME': cparsers.string.word('Welcome'),
#         'WORLD': cparsers.string.word('World'),
#         'NUMBER': cparsers.string.sint(),

#         'SPC': cparsers.string.word(' '),
#     }

#     maps: dict[str, Callable[[cparsers.Status], Any]] = {
#         'unwraparr': lambda s: [item[0] for item in s.result],
#         'id': lambda s: s.result,
#     }

#     for definition in result.result:
#         name, parser = compile_def(definition, glob, maps)

#         glob[name] = parser

#     r = glob['TARGET'].run(cparsers.Status('Hello World 334 565 2137 '))
#     print_result(r)