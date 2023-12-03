from utils.inputs import get_input


def parse_nums(line):
    return int(next(filter(str.isnumeric, line)) + next(filter(str.isnumeric, "".join(reversed(line)))))


def replace_nums(line):
    replacements = [
        ("one", "1"),
        ("two", "2"),
        ("three", "3"),
        ("four", "4"),
        ("five", "5"),
        ("six", "6"),
        ("seven", "7"),
        ("eight", "8"),
        ("nine", "9"),
    ]
    earliest_num, latest_num = next(filter(str.isnumeric, line)), next(filter(str.isnumeric, "".join(reversed(line))))
    earliest_index, latest_index = line.find(earliest_num), line.rfind(latest_num)
    earliest_word, latest_word = "", ""
    for s, n in replacements:
        first = line.find(s, None, earliest_index + 1) # +1 to account for overlapping letters, tricky!
        if first > -1:
            earliest_index = first
            earliest_word = n

        last = line.rfind(s, latest_index)
        if last > latest_index:
            latest_index = last
            latest_word = n

    if earliest_word:
        earliest_num = earliest_word
    if latest_word:
        latest_num = latest_word
    return int(earliest_num + latest_num)


def part_one(data):
    return sum(map(parse_nums, data))


def part_two(data):
    return sum(map(replace_nums, data))


def run_sample():
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=True)
        print(f"{f.__name__}:\n\t{f(data)}")


def run_actual():
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=False)
        print(f"{f.__name__}:\n\t{f(data)}")


if __name__ == "__main__":
    run_sample()
    run_actual()
