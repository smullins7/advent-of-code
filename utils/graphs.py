from dataclasses import dataclass, field
from typing import Any, Dict, List, TextIO, Set


@dataclass
class NDimPoint:
    position: tuple
    value: Any = None

    def __hash__(self):
        return hash(self.position)

    def __str__(self):
        return " ".join([str(p) for p in [self.position, self.value or ""]])


@dataclass
class NDimGraph:
    points: Dict[tuple, NDimPoint] = field(default_factory=dict)
    value_index: Dict[Any, NDimPoint] = field(default_factory=dict)
    current: NDimPoint = None

    def add_point(self, *position, value=None):
        self.points[position] = NDimPoint(position, value)
        if value:
            self.value_index[value] = self.points[position]
        self.current = self.points[position]

    def move(self, *position, value=None):
        current = self.current.position
        if len(position) != len(current):
            raise ValueError(f"Must provide all dimensions when moving, {position} incompatible with {current}")
        self.add_point(*tuple(map(sum, zip(current, position))), value=value)

    def has(self, value):
        return value in self.value_index

    def get_by_value(self, value):
        return self.value_index.get(value)

    def pretty_print(self):
        for point in self.points.values():
            print(point)


@dataclass
class TwoDGrid:
    points: List[List[Any]] = field(default_factory=list)

    def get_row(self, row_index):
        return self.points[row_index]

    def get_column(self, column_index):
        return [self.points[i][column_index] for i in range(len(self.points))]

    def pretty_print(self):
        for row in self.points:
            print(" ".join(row))

    @classmethod
    def from_file(cls, open_file: TextIO):
        line = open_file.readline()
        grid = TwoDGrid()
        while line:
            grid.points.append([x.strip() for x in line.split(" ") if x.strip()])
            line = open_file.readline()
        return grid


@dataclass(unsafe_hash=True)
class SparseValueGrid:
    values: dict
    max_x: int = None
    min_x: int = None
    max_y: int = None
    min_y: int = None
    cursor_x: int = 0
    cursor_y: int = 0

    def set(self, x, y, val):
        self.values[(x, y)] = val
        self.max_x = max(self.max_x, x) if self.max_x is not None else x
        self.min_x = min(self.min_x, x) if self.min_x is not None else x
        self.max_y = max(self.max_y, y) if self.max_y is not None else y
        self.min_y = min(self.min_y, y) if self.min_y is not None else y

    def get(self, x, y, default=None):
        return self.values.get((x, y), default)

    def has(self, x, y):
        return (x, y) in self.values

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.values[(self.cursor_x, self.cursor_y)]
            x, y = self.cursor_x, self.cursor_y
        except KeyError:
            self.cursor_x = 0
            self.cursor_y = 0
            raise StopIteration
        if self.cursor_x == self.max_x:
            self.cursor_y += 1
            self.cursor_x = 0
        else:
            self.cursor_x += 1
        return x, y, result


@dataclass(unsafe_hash=True)
class SparseGrid:
    values: set = field(default_factory=lambda: set())
    max_x: int = None
    max_y: int = None
    min_x: int = None
    min_y: int = None

    def set(self, x, y):
        self.values.add((x, y))
        self.max_x = max(self.max_x, x) if self.max_x is not None else x
        self.min_x = min(self.min_x, x) if self.min_x is not None else x
        self.max_y = max(self.max_y, y) if self.max_y is not None else y
        self.min_y = min(self.min_y, y) if self.min_y is not None else y

    def has(self, x, y):
        return (x, y) in self.values

    def __iter__(self):
        return iter(self.values)


@dataclass(unsafe_hash=True)
class Cell:
    x: int
    y: int
    value: Any

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.value == other.value

    def __str__(self):
        return f"({self.x}, {self.y}, {self.value})"


@dataclass
class Grid:
    """
    A two-dimensional array, where the number of rows (y) is not assumed to equal the number of columns (x).
    x and y are never negative, so this does not resemble a numerical graph.
    """
    rows: List[List[Cell]]

    def find_neighbors(self, cell) -> List[Cell]:
        return self.find_adjacency(cell.x, cell.y)

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

    def as_adjacency_list(self) -> Dict[Cell, List[Cell]]:
        adjacency = {}
        for row in self:
            for cell in row:
                adjacency[cell] = self.find_neighbors(cell)
        return adjacency

    def __iter__(self):
        return iter(self.rows)


@dataclass
class Node:
    value: str
    neighbors: Set  # of Node

    def add_path(self, node):
        self.neighbors.add(node)
        node.neighbors.add(self)

    @staticmethod
    def from_value(value):
        return Node(value, set())

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, o) -> bool:
        return self.value == o.value

    def __iter__(self):
        return iter(self.neighbors)
