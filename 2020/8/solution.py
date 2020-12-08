def part1(inputs):
    return attempt(inputs)[0]


def part2(inputs):
    for i, instruction in enumerate(inputs):
        if instruction.startswith("acc"):
            continue
        elif instruction.startswith("nop"):
            replaced = instruction.replace("nop", "jmp")
            acc, looped = attempt(inputs[:i] + [replaced] + inputs[i + 1:])
            if not looped:
                return acc

        elif instruction.startswith("jmp"):
            replaced = instruction.replace("jmp", "nop")
            acc, looped = attempt(inputs[:i] + [replaced] + inputs[i + 1:])
            if not looped:
                return acc

def attempt(inputs):
    visited = set()
    acc = 0
    cursor = 0
    while cursor not in visited and cursor < len(inputs):
        instruction = inputs[cursor]
        visited.add(cursor)
        op, value = instruction.split(" ")
        value = int(value)
        if op == "nop":
            cursor += 1
            continue
        elif op == "acc":
            acc += value
            cursor += 1
            continue
        cursor += value
    return acc, cursor < len(inputs)


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")]
    print(part1(inputs))
    print(part2(inputs))
