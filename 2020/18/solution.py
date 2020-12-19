import re

PARENS = re.compile('.*\(([^(]+?)\).*')

ADDITION = re.compile('\d+ \+ \d+')


def run(lines, eval_fun, addition_precedence=False):
    return sum([parse(line, eval_fun, addition_precedence) for line in lines])


def parse(line, eval_fun, addition_precedence=False):
    parens = PARENS.search(line)
    while parens:
        line = line[:parens.start(1) - 1] + str(parse(parens.group(1), eval_fun, addition_precedence)) + line[parens.end(1) + 1:]
        parens = PARENS.search(line)

    if addition_precedence:
        addition = ADDITION.search(line)
        while addition:
            line = line[:addition.start()] + str(eval_fun(addition.group(0))) + line[addition.end():]
            addition = ADDITION.search(line)

    return eval_fun(line)


def left_to_right(line):
    symbols = line.split(" ")
    exp = symbols[0]
    for symbol in symbols[1:]:
        exp += symbol
        if symbol.isdigit():
            exp = str(eval(exp))
    return int(exp)


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input")]
    print(run(inputs, left_to_right))
    print(run(inputs, eval, True))

