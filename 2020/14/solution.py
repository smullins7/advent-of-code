def do_mask(mask, value):
    bits = list('{0:036b}'.format(int(value)))
    for i, c in enumerate(mask):
        if c == "X":
            continue
        bits[i] = c
    return "".join(bits)


def part1(inputs):
    memory = {}
    mask = None
    for line in inputs:
        left, right = line.split(" = ")
        if left == "mask":
            mask = right
        else:
            memory[left] = do_mask(mask, right)

    return sum([int(n, 2) for n in memory.values()])


def do_mask2(mask, value):
    bits = list('{0:036b}'.format(int(value)))
    for i, c in enumerate(mask):
        if c == "0":
            continue
        bits[i] = c
    return bits


def part2(inputs):
    memory = {}
    mask = None
    for line in inputs:
        left, right = line.split(" = ")
        if left == "mask":
            mask = right
        else:
            addresses = []
            masked = do_mask2(mask, left[4:-1])
            masks = masked.count("X")
            for i in range(2**masks):
                value_bits = list(("{0:0%db}" % masks).format(i))
                new_value = list(masked)
                for j, c in enumerate(new_value):
                    if c == "X":
                        new_value[j] = value_bits.pop(0)
                addresses.append(int("".join(new_value), 2))
            for address in addresses:
                memory[address] = right

    return sum([int(n) for n in memory.values()])


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")]
    #print(part1(inputs))
    print(part2(inputs))

