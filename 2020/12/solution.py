
dirs = ["W", "N", "E", "S"]


def get_dir(d):
    return dirs[d % len(dirs)]


def part1(inputs):
    position = 0, 0
    facing = 2
    for nav in inputs:
        action = nav[0]
        value = int(nav[1:])

        if action in ["N", "S", "E", "W"]:
            position = move(position, action, value)
        elif action == "F":
            position = move(position, get_dir(facing), value)
        elif action == "L":
            facing -= int(value/90)
        elif action == "R":
            facing += int(value/90)

    return abs(position[0]) + abs(position[1])


def move(position, action, value):
    if action == "N":
        return position[0], position[1] + value
    elif action == "S":
        return position[0], position[1] - value
    elif action == "E":
        return position[0] + value, position[1]
    elif action == "W":
        return position[0] - value, position[1]


def part2(inputs):
    ship = 0, 0
    waypoint = 10, 1
    for nav in inputs:
        action = nav[0]
        value = int(nav[1:])

        if action == "N":
            waypoint = waypoint[0], waypoint[1] + value
        elif action == "S":
            waypoint = waypoint[0], waypoint[1] - value
        elif action == "E":
            waypoint = waypoint[0] + value, waypoint[1]
        elif action == "W":
            waypoint = waypoint[0] - value, waypoint[1]
        elif action == "L":
            if value == 90:
                waypoint = -waypoint[1], waypoint[0]
            elif value == 180:
                waypoint = -waypoint[0], -waypoint[1]
            elif value == 270:
                waypoint = waypoint[1], -waypoint[0]
        elif action == "R":
            if value == 90:
                waypoint = waypoint[1], -waypoint[0]
            elif value == 180:
                waypoint = -waypoint[0], -waypoint[1]
            elif value == 270:
                waypoint = -waypoint[1], waypoint[0]
        elif action == "F":
            ship = ship[0] + (value * waypoint[0]), ship[1] + (value * waypoint[1])

    return abs(ship[0]) + abs(ship[1])


if __name__ == "__main__":
    inputs = [line.strip() for line in open("./input.txt")]
    print(part1(inputs))
    # not 46768
    print(part2(inputs))
