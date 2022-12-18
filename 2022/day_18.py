from utils.inputs import get_input


def parse(line):
    return tuple([int(v) for v in line.split(",")])


def part_one(data):
    all_points = set()
    for point in data:
        all_points.add(point)

    total_surface_area = 0
    for (x, y, z) in all_points:
        surface_area = 6
        if (x - 1, y, z) in all_points:
            surface_area -= 1
        if (x + 1, y, z) in all_points:
            surface_area -= 1
        if (x, y + 1, z) in all_points:
            surface_area -= 1
        if (x, y - 1, z) in all_points:
            surface_area -= 1
        if (x, y, z + 1) in all_points:
            surface_area -= 1
        if (x, y, z - 1) in all_points:
            surface_area -= 1

        total_surface_area += surface_area
    return total_surface_area


def get_nondiagonal_neighbors(x, y, z):
    return [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]


class Space:

    def __init__(self, points):
        self.points = set(points)
        self.min_x = min([p[0] for p in points])
        self.max_x = max([p[0] for p in points])
        self.min_y = min([p[1] for p in points])
        self.max_y = max([p[1] for p in points])
        self.min_z = min([p[2] for p in points])
        self.max_z = max([p[2] for p in points])

    def add(self, x, y, z):
        self.points.add((x, y, z))

    def within(self, x, y, z):
        return (self.min_x <= x <= self.max_x) and (self.min_y <= y <= self.max_y) and (self.min_z <= z <= self.max_z)


def air_neighbors(space: Space, x, y, z):
    return [(neighbor_x, neighbor_y, neighbor_z) for neighbor_x, neighbor_y, neighbor_z in get_nondiagonal_neighbors(x, y, z)
            if (neighbor_x, neighbor_y, neighbor_z) not in space.points]


def part_two(data):
    space = Space(data)

    all_air_points = set()
    for x in range(space.min_x +1, space.max_x):
        for y in range(space.min_y+1, space.max_y):
            for z in range(space.min_z+1, space.max_z):
                if (x, y, z) not in space.points:
                    all_air_points.add((x, y, z))

    air_pockets = set()
    for (x, y, z) in all_air_points:
        to_check = air_neighbors(space, x, y, z)

        seen = set()
        infinite_space = False
        while to_check:
            possible_x, possible_y, possible_z = to_check.pop()
            if (
                not space.min_x <= possible_x <= space.max_x or
                not space.min_y <= possible_y <= space.max_y or
                not space.min_z <= possible_z <= space.max_z
            ):
                # we have drifted out into infinite space now so this is not an air pocket
                infinite_space = True
                break
            if (possible_x, possible_y, possible_z) in seen:
                continue
            seen.add((possible_x, possible_y, possible_z))
            to_check.extend(air_neighbors(space, possible_x, possible_y, possible_z))
        if not infinite_space:
            air_pockets.add((x, y, z))

    air_surface_area = 0
    for x, y, z in air_pockets:
        for neighbor_x, neighbor_y, neighbor_z in get_nondiagonal_neighbors(x, y, z):
            if (neighbor_x, neighbor_y, neighbor_z) in space.points:
                air_surface_area += 1

    return part_one(data) - air_surface_area


# 2681 too high, 2063 is wrong
if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0, coerce=parse)
        print(f"{f.__name__}:\n\t{f(data)}")
