from itertools import combinations

from utils.inputs import get_inputs, get_grouped_inputs

def apply(g, w1, w2):
    if g == "AND":
        return w1 and w2
    elif g == "OR":
        return w1 or w2
    elif g == "XOR":
        return w1 ^ w2

def part_one(data):
    wires, gates = data
    wired = {}
    for wire in wires:
        wire, value = wire.split(": ")
        wired[wire] = bool(int(value))

    todo = [gate.split(" ") for gate in gates]
    resolved = {}
    while todo:
        w1, g, w2, _, w3 = todo.pop(0)
        if w1 in wired and w2 in wired:
            value = apply(g, wired[w1], wired[w2])
            if w3.startswith("z"):
                resolved[w3] = value
            else:
                wired[w3] = value
        else:
            todo.append([w1, g, w2, _, w3])

    bits = [0] * len(resolved)
    for k, v in resolved.items():
        bits[int(k[1:])] = int(v)
    return int("".join([str(b) for b in reversed(bits)]), 2)


def is_xy_wire(w: str):
    return w.startswith("x") or w.startswith("y")

def _recurse(lookups: dict[str,tuple], key:str) -> tuple:
    w1, g, w2 = lookups[key]
    if (w1.startswith("x") or w1.startswith("y")) and (w2.startswith("x") or w2.startswith("y")):
        return w1, g, w2
    elif w1.startswith("x") or w1.startswith("y"):
        return w1, g, _recurse(lookups, w2)
    elif w2.startswith("x") or w2.startswith("y"):
        return _recurse(lookups, w1), g, w2

    return _recurse(lookups, w1), g, _recurse(lookups, w2)

def find_gates_involved_with(lookups: dict[str,tuple], key: str, seen: set):
    w1, g, w2 = lookups[key]
    seen.add(w1)
    seen.add(w2)
    if not is_xy_wire(w1):
        find_gates_involved_with(lookups, w1, seen)
    if not is_xy_wire(w2):
        find_gates_involved_with(lookups, w2, seen)

def attempt(gates, swap1, swap2):
    wired = {}
    for i in range(45):
        wired[f"x{i:02d}"] = 0
        wired[f"y{i:02d}"] = 1

    todo = []
    for gate in gates:
        w1, g, w2, _, w3 = gate.split(" ")
        if w3 == swap1:
            todo.append((w1, g, w2, swap2))
        elif w3 == swap2:
            todo.append((w1, g, w2, swap1))
        else:
            todo.append((w1, g, w2, w3))
    resolved = {}
    i = 0
    while todo:
        w1, g, w2, w3 = todo.pop(0)
        if w3 in (w1, w2):
            return "this swap resulted in infinite recursion, abandoning"
        if w1 in wired and w2 in wired:
            value = apply(g, wired[w1], wired[w2])
            if w3.startswith("z"):
                resolved[w3] = value
            else:
                wired[w3] = value
        else:
            todo.append((w1, g, w2, w3))

        i += 1
        if i > 100000:
            return "this swap resulted in something bad"

    bits = [0] * len(resolved)
    for k, v in resolved.items():
        bits[int(k[1:])] = int(v)
    return "".join([str(b) for b in reversed(bits)])

def part_two(data):
    wires, gates = data
    lookup = {}
    for gate in gates:
        w1, g, w2, _, w3 = gate.split(" ")
        lookup[w3] = (w1, g, w2)







    #for i in range(45):
    #    print(_recurse(lookup, f"z{i:02d}"))

    for gate in gates:
        w1, g, w2, _, w3 = gate.split(" ")
        if w3.startswith("z") and g != "XOR":
            print(w3, ": ", w1, g, w2)

    seen = set()
    seen.add("z11")
    find_gates_involved_with(lookup, "z11", seen)

    seen10 = set()
    find_gates_involved_with(lookup, "z10", seen10)

    print(attempt(gates, None, None))
    maybes = [w for w in seen.difference(seen10) if not is_xy_wire(w)]
    for swaps in combinations(maybes, 2):
        print(swaps)
        print(attempt(gates, *swaps))


if __name__ == "__main__":
    sample_data, real_data = get_grouped_inputs(__file__)
    for f in (part_one, part_two):
        #print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")