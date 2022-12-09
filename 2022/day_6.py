from lib_inputs import get_input


def check_for_something(i, data, magic_num):
    look_behind = data[i:i + magic_num]
    return len(set(look_behind)) == magic_num


def loop(data, magic_num):
    for i, c in enumerate(data[magic_num - 1:]):
        if check_for_something(i, data, magic_num):
            return i + magic_num


def part_one(data):
    return loop(data, 4)


def part_two(data):
    return loop(data, 14)


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")
