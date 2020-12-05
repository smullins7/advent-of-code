def mid(a, b):
    return round((a + b) / 2)


def bisect(seat, c):
    if c == "F":
        lower, upper = seat["rows"]
        seat["rows"] = lower, mid(lower, upper)
    elif c == "B":
        lower, upper = seat["rows"]
        m = mid(lower, upper)
        seat["rows"] = m if m != lower else upper, upper
    elif c == "L":
        lower, upper = seat["columns"]
        seat["columns"] = lower, mid(lower, upper)
    elif c == "R":
        lower, upper = seat["columns"]
        m = mid(lower, upper)
        seat["columns"] = m if m != lower else upper, upper


def part1(inputs):
    seat_ids = []
    for assignment in inputs:
        seat = {
            "rows": (0, 127),
            "columns": (0, 7),
        }
        for cmd in assignment:
            bisect(seat, cmd)
        seat_ids.append(seat["rows"][0] * 8 + seat["columns"][0])
    return seat_ids


def part2(inputs):
    prev = None
    for seat_id in sorted(part1(inputs)):
        if not prev:
            prev = seat_id
            continue
        if seat_id - 1 != prev:
            return seat_id - 1
        prev = seat_id


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")]
    print(max(part1(inputs)))
    print(part2(inputs))
