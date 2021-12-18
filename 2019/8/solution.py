

def to_layers(data, read_size):
    layers = []
    c = 0
    while c < len(inputs):
        layers.append("".join([data[c + i] for i in range(read_size)]))
        c += read_size
    return layers

def part1(inputs, wide, tall):
    layers = to_layers(inputs, wide * tall)

    best_layer = None
    for layer in layers:
        count = layer.count("0")
        if not best_layer or best_layer.count("0") > count:
            best_layer = layer

    return int(best_layer.count("1")) * int(best_layer.count("2"))


def part2(inputs, wide, tall):
    layers = to_layers(inputs, wide * tall)
    resolved = []
    for zipped in zip(*layers):
        for b in zipped:
            if b == "2":
                continue
            break
        resolved.append(b)

    for i in range(tall):
        print("".join(["X" if c == "1" else " " for c in resolved[i*wide:(i+1)*wide]]))
    return 0


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")][0]
    #print(part1(inputs, 25, 6))
    print(part2(inputs, 25, 6))

