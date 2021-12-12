#!/usr/bin/env python3
from collections import defaultdict
from copy import copy
from lib_inputs import to_nodes


def part_one(start):
    def dfs(visited, node, this_path, all_paths):
        if node.value == "end":
            all_paths.add(",".join(this_path + ["end"]))
            return
        if node.value.islower() and node.value in visited:
            # this path is invalid and should be stopped
            return
        if node.value.islower():
            visited.add(node.value)
        this_path.append(node.value)
        for neighbour in node:
            dfs(set(visited), neighbour, list(this_path), all_paths)

    paths = set()
    dfs(set(), start, [], paths)
    return len(paths)


def part_two(start):
    def dfs(visited, node, this_path, all_paths):
        if node.value == "end":
            all_paths.add(",".join(this_path + ["end"]))
            return
        if node.value == "start" and node.value in visited:
            return
        if node.value.islower() and node.value in visited and max(visited.values()) == 2:
            # this path is invalid and should be stopped
            return
        if node.value.islower():
            visited[node.value] += 1
        this_path.append(node.value)
        for neighbour in node:
            dfs(copy(visited), neighbour, list(this_path), all_paths)
    paths = set()
    dfs(defaultdict(int), start, [], paths)
    return len(paths)


if __name__ == "__main__":
    for puzzle in ("sample", "sample2", "sample3", 1):
        for f in (part_one, part_two):
            start = to_nodes(__file__, puzzle)
            print(f"{f.__name__}: Input {puzzle}, {f(start)}")
