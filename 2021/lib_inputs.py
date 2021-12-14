from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import List, Set

DAY_RE = re.compile(r"^.*/day_(\d+)\.py$")
BASE_PATH = os.path.dirname(__file__)


def day_filename(filename, puzzle):
    return f"{BASE_PATH}/inputs/day-{DAY_RE.match(filename).group(1)}-{puzzle}.txt"


def get_input(filename, puzzle=1, coerce=str):
    parsed = [coerce(x.strip()) for x in open(day_filename(filename, puzzle)).readlines()]
    # some puzzle inputs are only a single line and meant to be split on some delimiter
    return parsed if len(parsed) > 1 else parsed[0]


def to_grid(filename, puzzle=1, coerce=int):
    grid = Grid([])
    for y, line in enumerate(open(day_filename(filename, puzzle)).readlines()):
        grid.rows.append([Cell(x, y, coerce(c)) for x, c in enumerate(line.strip())])
    return grid


@dataclass(unsafe_hash=True)
class Cell:
    x: int
    y: int
    value: int

    def __str__(self):
        return f"({self.x}, {self.y}, {self.value})"


@dataclass
class Grid:
    """
    A two-dimensional array, where the number of rows (y) is not assumed to equal the number of columns (x).
    x and y are never negative, so this does not resemble a numerical graph.
    """
    rows: List[List[Cell]]

    def find_adjacency(self, x, y) -> List[Cell]:
        adjacency = []
        row = self.rows[y]
        if y != 0:
            adjacency.append(self.rows[y - 1][x])
        if y != len(self.rows) - 1:
            adjacency.append(self.rows[y + 1][x])
        if x != 0:
            adjacency.append(row[x - 1])
        if x != len(row) - 1:
            adjacency.append(row[x + 1])
        return adjacency

    def find_diagonal_adjacency(self, x, y) -> List[Cell]:
        adjacency = []
        row = self.rows[y]
        if y != 0:
            if x != 0:
                adjacency.append(self.rows[y - 1][x - 1])
            if x != len(row) - 1:
                adjacency.append(self.rows[y - 1][x + 1])
        if y != len(self.rows) - 1:
            if x != 0:
                adjacency.append(self.rows[y + 1][x - 1])
            if x != len(row) - 1:
                adjacency.append(self.rows[y + 1][x + 1])
        return adjacency

    def find_all_adjacency(self, x, y) -> List[Cell]:
        return self.find_adjacency(x, y) + self.find_diagonal_adjacency(x, y)

    def __iter__(self):
        return iter(self.rows)


@dataclass
class Node:
    value: str
    neighbors: Set[Node]

    def add_path(self, node):
        self.neighbors.add(node)
        node.neighbors.add(self)

    @staticmethod
    def from_value(value):
        return Node(value, set())

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, o: Node) -> bool:
        return self.value == o.value

    def __iter__(self):
        return iter(self.neighbors)


def to_nodes(filename, puzzle=1) -> Node:
    nodes = {}

    def _get(value) -> Node:
        if value not in nodes:
            nodes[value] = Node.from_value(value)
        return nodes[value]

    for line in open(day_filename(filename, puzzle)).readlines():
        left, right = line.strip().split("-")
        left_node = _get(left)
        right_node = _get(right)
        left_node.add_path(right_node)
    return nodes["start"]
