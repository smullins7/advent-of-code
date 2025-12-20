from itertools import combinations

from utils.graphs import SparseGrid
from utils.inputs import get_inputs


def area(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def part_one(data):
    grid = SparseGrid()
    for line in data:
        grid.set(*[int(n) for n in line.split(",")])

    return max([area(a, b) for a, b in combinations(grid, 2)])


def part_two(data):
    points = []
    s = set()
    for line in data:
        x, y = [int(n) for n in line.split(",")]
        points.append((x, y))
        s.add((x, y))

    max_area = 0
    for a, b in combinations(points, 2):
        if a[0] == b[0] or a[1] == b[1] or ((a[0], b[1]) in s and (b[0], a[1]) in s):
            max_area = max(max_area, area(a, b))
        elif within(points, a[0], b[1]) and within(points, b[0], a[1]):
            max_area = max(max_area, area(a, b))
    return max_area


def within(ordered_points, x, y):
    num_vertices = len(ordered_points)
    inside = False
    a = ordered_points[0]

    for i in range(1, num_vertices + 1):
        b = ordered_points[i % num_vertices]

        if (x, y) in [a, b]:
            return True

        if a[0] <= x <= b[0] and y == a[1] and y == b[1]:
            return True
        if a[1] <= y <= b[1] and x == a[0] and x == b[0]:
            return True

        # Check if the point is above the minimum y coordinate of the edge
        if y > min(a[1], b[1]):
            # Check if the point is below the maximum y coordinate of the edge
            if y <= max(a[1], b[1]):
                # Check if the point is to the left of the maximum x coordinate of the edge
                if x <= max(a[0], b[0]):
                    # Calculate the x-intersection of the line connecting the point to the edge
                    x_intersection = (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1]) + a[0]

                    # Check if the point is on the same line as the edge or to the left of the x-intersection
                    if a[0] == b[0] or x <= x_intersection:
                        # Flip the inside flag
                        inside = not inside

        # Store the current point as the first point for the next iteration
        a = b

    # Return the value of the inside flag
    return inside


if __name__ == "__main__":
    sample_data, real_data = get_inputs(__file__)
    for f in (part_one, part_two):
        print(f"{f.__name__} sample:\n\t{f(sample_data)}")
        print(f"{f.__name__}:\n\t{f(real_data)}")
# 4629483216 too high
