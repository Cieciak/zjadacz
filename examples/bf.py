from zjadacz import *

from zjadacz.string import *

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


class AST_runner:

    def __init__(self, mem_size: int = 30_000):
        self.memory = [0, ] * mem_size
        self.pointer = 0

    def run(self, tree: Status):
        for element in tree:
            if isinstance(element, dict):
                key, *_ = element.keys()
                val, *_ = element.values()
            else:
                key = element

            match key:

                case '+':
                    self.memory[self.pointer] = (self.memory[self.pointer] + val) % 256
                case '-':
                    self.memory[self.pointer] = (self.memory[self.pointer] - val) % 256
                case '>':
                    self.pointer = (self.pointer + val) % len(self.memory)
                case '<':
                    self.pointer = (self.pointer - val) % len(self.memory)
                case 'loop':
                    while self.memory[self.pointer] != 0:
                        self.run(val)
                case '.':
                    print(chr(self.memory[self.pointer]), end='')
                case ',':
                    self.memory[self.pointer] = ord(input()[0])

if __name__ == '__main__':
    s = Status('+++++++++++[[>>]++++++++++[>++++++++++<-]+[<<]>>-]>>>-.>>+++++.>>+.>>-.>>+++++.>>---.>>+++++++.>>[-]<+++++[>++++++++<-]>--.>>.>>+.>>++++++++++++++++++.>++++++++++.')

    r = prog.run(s)
    runner = AST_runner()
    runner.run(r.result)