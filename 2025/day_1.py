from utils.inputs import get_inputs

cap = 100


def part_one(data):
    cursor = 50
    at_zero = 0
    for line in data:
        direction = line[0]
        amount = int(line[1:])
        cursor = (cursor - amount if direction == 'L' else cursor + amount) % cap
        if cursor == 0:
            at_zero += 1
    return at_zero


def part_two(data):
    cursor = 50
    touched_zero = 0
    for line in data:
        direction = line[0]
        amount = int(line[1:])
        prev = cursor
        cursor = (cursor - amount if direction == 'L' else cursor + amount)
        # print(prev, direction, amount,
        #      int((prev + amount if direction == 'R' or prev == 0 else cap - prev + amount) / cap))
        touched_zero += int((prev + amount if direction == 'R' or prev == 0 else cap - prev + amount) / cap)
        cursor = cursor % cap
    return touched_zero


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
