from lib_inputs import get_input


class Rope:

    def __init__(self, num_of_knots=2):
        self.knots = [(0, 0)] * num_of_knots
        self.history = {(0, 0)}

    def move(self, direction):
        head = self.knots[0]
        # up
        if direction == "U":
            head = head[0], head[1] + 1
        # down
        elif direction == "D":
            head = head[0], head[1] - 1
        # left
        elif direction == "L":
            head = head[0] - 1, head[1]
        # right
        else:
            head = head[0] + 1, head[1]

        self.knots[0] = head
        self._move_knots()

    def _move_knots(self):
        leader = self.knots[0]
        moved_knots = [leader]
        for knot in self.knots[1:]:
            moved = self._move_knot(leader, knot)
            leader = moved
            moved_knots.append(moved)

        self.knots = moved_knots
        self.history.add(self.knots[-1])

    @staticmethod
    def _move_knot(leader, follower):
        # if head and tail are co-located or adjacent, nothing to do
        if abs(leader[1] - follower[1]) <= 1 and abs(leader[0] - follower[0]) <= 1:
            return follower

        # if head and tail are same row
        if leader[1] == follower[1]:
            # head is to the right of tail
            if leader[0] > follower[0]:
                follower = follower[0] + 1, follower[1]
            else:
                follower = follower[0] - 1, follower[1]
        # if head and tail are same column
        elif leader[0] == follower[0]:
            # head is above tail
            if leader[1] > follower[1]:
                follower = follower[0], follower[1] + 1
            else:
                follower = follower[0], follower[1] - 1
        # diagonal skip
        else:
            # move up
            if leader[1] > follower[1]:
                follower = follower[0], follower[1] + 1
            # move down
            else:
                follower = follower[0], follower[1] - 1

            # move left
            if follower[0] > leader[0]:
                follower = follower[0] - 1, follower[1]
            # move right
            else:
                follower = follower[0] + 1, follower[1]

        return follower


def part_one(data):
    rope = Rope()

    for move in data:
        direction, scalar = move.split(" ")
        for _ in range(int(scalar)):
            rope.move(direction)

    return len(rope.history)


def part_two(data):
    rope = Rope(num_of_knots=10)

    for move in data:
        direction, scalar = move.split(" ")
        for _ in range(int(scalar)):
            rope.move(direction)

    return len(rope.history)


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0)
        print(f"{f.__name__}:\n\t{f(data)}")
