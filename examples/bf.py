from cparsers import *

#
# INST ::= ["+"? | "-"? | ">"? | "<"? | "." | "?" | LOOP]
#

inst = choiceOf(
    many(word('+'), strict=True),
    many(word('-'), strict=True),
    many(word('>'), strict=True),
    many(word('<'), strict=True),
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
    s = Status('[>+++<-]')

    r = prog.run(s)

    print(r)