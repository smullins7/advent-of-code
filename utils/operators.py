import operator

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def from_op_string(s: str) -> ():
    return OPS[s]
