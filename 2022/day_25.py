from utils.inputs import get_input

OPS = {
    "2": lambda n: n * 2,
    "1": lambda n: n * 1,
    "0": lambda n: 0,
    "-": lambda n: -n,
    "=": lambda n: -2 * n,
}

CHECK = ("2", "1", "0", "-", "=")


def snafu_to_base_10(s: str) -> int:
    return sum([OPS[c](pow(5, i)) for i, c in enumerate(reversed(s))])


def lowest(s: str) -> str:
    return "=" * len(s)


def snafu_digit(n: int, upper: str, index: int) -> str:
    for check in CHECK:
        remaining = upper[index + 1:]
        if snafu_to_base_10(upper[0:index] + check + lowest(remaining)) <= n <= snafu_to_base_10(
                upper[0:index] + check + remaining):
            return check


def base_10_to_snafu(n: int) -> str:
    temp = "2"
    while snafu_to_base_10(temp) < n:
        temp += "2"

    for index in range(len(temp)):
        c = snafu_digit(n, temp, index)
        temp = temp[0:index] + c + temp[index + 1:]

    return temp


def part_one(data):
    total = sum([snafu_to_base_10(s) for s in data])
    print(total)
    return base_10_to_snafu(total)


def part_two(data):
    return 0


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")
