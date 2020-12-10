from functools import reduce


def part1(inputs):
    one_diff = 0
    three_diff = 1
    prev = None
    for adapter in sorted(inputs + [0]):
        if prev is None:
            prev = adapter
            continue
        diff = adapter - prev
        if diff == 1:
            one_diff += 1
        elif diff == 3:
            three_diff += 1

        prev = adapter

    return one_diff * three_diff


def part2(inputs):
    valid = []
    # last adapter must always be present
    adapters = sorted(inputs)

    groups = []
    group = []
    for adapter in adapters:
        if not group:
            group.append(0)
            group.append(adapter)
            continue

        if adapter - group[-1] == 3:
            print(len(group))
            groups.append(group)
            group = [adapter]
            continue

        group.append(adapter)

    if group != groups[-1]:
        groups.append(group)

    for group in groups:
        if len(group) < 3:
            valid.append(1)
            continue
        if len(group) == 3:
            valid.append(2)
            continue
        if len(group) == 4:
            if group[-1] - group[0] == 3:
                valid.append(4)
            else:
                print(group)
        elif len(group) == 5:
            if group[-1] - group[0] == 4:
                valid.append(7)
            else:
                print(group)
        else:
            print(group)

    return reduce(lambda x, y: x * y, valid)


"""
def foo():
    #print(len(groups))
    #print(groups)
    
        #print(len(group))

    #print(valid)


    prev = 0
    options = 0
    adapters = sorted(inputs)
    for i, adapter in enumerate(adapters):
        if i == len(adapters) - 1:
            break

        if adapter - prev < 3 and adapters[i+1] - adapter < 3:
            options += 1
        prev = adapter

    #print(reduce(lambda x, y: x * y, valid))

    print(options)
    return 2**options


def is_valid(adapters):
    prev = None
    for adapter in sorted(adapters):
        if prev is None:
            prev = adapter
            continue
        if adapter - prev > 3:
            return False

    return True
"""

if __name__ == "__main__":
    inputs = [int(line.strip()) for line in open("./input.txt")]
    print(part1(inputs))
    print(part2(inputs))
