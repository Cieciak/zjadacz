import cparsers
import cparsers.string


identifier = cparsers.string.regex("[A-Z]+")
walrus = cparsers.string.word("::=")


def build_parser():
    many = cparsers.sequenceOf(
        cparsers.string.word("("),
        cparsers.lazy(lambda: expr),
        cparsers.many(
            cparsers.sequenceOf(
                cparsers.string.word(" "),
                cparsers.lazy(lambda: expr),
            ).map(lambda s: s.result[1::2])
        ).map(lambda s: [item[0] for item in s.result]),
        cparsers.string.word(")"),
    ).map(lambda s: {"seqence": [s.result[1], *s.result[2]]})

    expr = cparsers.choiceOf(
        many,
        identifier,
    )

    definition = cparsers.sequenceOf(
        identifier,
        walrus,
        expr,
        cparsers.string.word("\n")
    )

    parser = cparsers.many(
        definition,
    )

    return parser

    
    

def load_file(path: str) -> str:

    with open(path, 'r') as file:
        data = file.read()

    return data

if __name__ == '__main__':
    path = "examples/rozwik/samples/01.roz"

    root = build_parser()
    data = load_file(path)

    print(data)

    result = root.run(cparsers.Status(data))

    print(result)