import re

from utils.inputs import get_inputs

GAME_PAT = re.compile(r"^Game (?P<game_num>\d+): (?P<pulls>.*)$")


def parse_game(line):
    m = GAME_PAT.match(line)
    cubes = []
    for pull_line in m.group("pulls").split("; "):
        blue, green, red = 0, 0, 0
        for cube_set in pull_line.split(", "):
            if cube_set.count("blue"):
                blue = int(cube_set.split(" ")[0])
            if cube_set.count("green"):
                green = int(cube_set.split(" ")[0])
            if cube_set.count("red"):
                red = int(cube_set.split(" ")[0])
        cubes.append((blue, green, red))

    return int(m.group("game_num")), cubes


def validate(line, max_red, max_green, max_blue):
    game_num, cubes = parse_game(line)
    for (blue, green, red) in cubes:
        if blue > max_blue or green > max_green or red > max_red:
            return 0
    return game_num


def part_one(data):
    max_red, max_green, max_blue = 12, 13, 14
    return sum([validate(line, max_red, max_green, max_blue) for line in data])


def part_two(data):
    s = 0
    for line in data:
        n, cubes = parse_game(line)
        max_blue, max_green, max_red = 0, 0, 0
        for (blue, green, red) in cubes:
            max_blue = max(max_blue, blue)
            max_green = max(max_green, green)
            max_red = max(max_red, red)
        s += (max_blue * max_green * max_red)
    return s


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
