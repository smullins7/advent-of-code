from utils.inputs import get_inputs


def to_nums(line):
    return [int(x) for x in line.strip().split(" ")]


def make_stacks(nums):
    stacks = [nums]
    for inners in stacks:
        if all(n == 0 for n in inners):
            break
        else:
            another = []
            for i in range(0, len(inners) - 1):
                another.append(inners[i + 1] - inners[i])
            stacks.append(another)
    return stacks


def part_one(data):
    sums = 0
    for nums in data:
        stacks = make_stacks(nums)
        sums += sum([l[-1] for l in stacks[:-1]])
    return sums


def part_two(data):
    sums = 0
    for nums in data:
        stacks = make_stacks(nums)
        sums += sum(-1 * num if i % 2 != 0 else num for i, num in enumerate([l[0] for l in stacks[:-1]]))
    return sums


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__, coerce=to_nums)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
