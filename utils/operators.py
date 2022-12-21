import operator

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

COUNTERS = {
    operator.add: operator.sub,
    operator.sub: operator.add,
    operator.mul: operator.truediv,
    operator.truediv: operator.mul,
}


def from_op_string(s: str) -> ():
    return OPS[s]


def counter_op(op_func: ()):
    return COUNTERS[op_func]
