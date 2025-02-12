from cparsers import *

#
# INST ::= ["+"? | "-"? | ">"? | "<"? | "." | "?" | LOOP]
#

inst = choiceOf(
    many(word('+'), strict=True).map(lambda s: {'+': len(s.result)}),
    many(word('-'), strict=True).map(lambda s: {'-': len(s.result)}),
    many(word('>'), strict=True).map(lambda s: {'>': len(s.result)}),
    many(word('<'), strict=True).map(lambda s: {'<': len(s.result)}),
    word('.'),
    word(','),
    lazy(lambda: loop),
)

#
# LOOP ::= "[" INST "]"
#

loop = sequenceOf(
    word('['),
    many(inst),
    word(']'),
).map(
    lambda s: {'loop': s.result[1]}
)

#
# PROG ::= INST*
#

prog = many(inst, strict=True)



if __name__ == '__main__':
    s = Status('++++[>+++[>++<-]<-]')

    r = prog.run(s)

    print(r)