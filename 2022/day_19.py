import re
from dataclasses import dataclass
from itertools import combinations_with_replacement
from typing import List

from utils.inputs import get_input

PARSE_PAT = re.compile(r"Blueprint (?P<id>\d+): Each ore robot costs (?P<ore>\d+) ore. Each clay robot costs (?P<clay_ore>\d+) ore. Each obsidian robot costs (?P<obsidian_ore>\d+) ore and (?P<obsidian_clay>\d+) clay. Each geode robot costs (?P<geode_ore>\d+) ore and (?P<geode_obsidian>\d+) obsidian.")


def parse(line):
    return Blueprint(
        **{k: int(v) for k, v in PARSE_PAT.match(line).groupdict().items()}
    )


def part_one(data):
    quality_levels = 0
    for blueprint in data:
        max_level = 0
        for priorities in prioritize(400):
            factory = Factory(blueprint)
            factory.operate_with_priority(list(priorities))
            max_level = max(max_level, factory.determine_quality_level())
        print(blueprint.id, max_level)
        quality_levels += max_level
    return quality_levels


def prioritize(n):
    return list(combinations_with_replacement(["obsidian", "clay", "ore"], n))

def part_two(data):
    return 0


@dataclass
class Blueprint:
    id: int
    ore: int
    clay_ore: int
    obsidian_ore: int
    obsidian_clay: int
    geode_ore: int
    geode_obsidian: int
    max_clay: int = 0

    def __post_init__(self):
        self.max_clay = self.obsidian_clay // self.ore


@dataclass
class Factory:
    blueprint: Blueprint
    minutes: int = 24
    ore: int = 0
    ore_robots: int = 1
    clay: int = 0
    clay_robots: int = 0
    obsidian: int = 0
    obsidian_robots: int = 0
    geode_robots: int = 0
    geodes_opened: int = 0

    def operate(self):
        while self.minutes:
            # try to build, subtract resources
            new_geode_robots, new_obsidian_robots, new_clay_robots, new_ore_robots = 0, 0, 0, 0
            while self.ore >= self.blueprint.geode_ore and self.obsidian >= self.blueprint.geode_obsidian:
                # make geode robot
                self.ore -= self.blueprint.geode_ore
                self.obsidian -= self.blueprint.geode_obsidian
                new_geode_robots += 1

            while self.ore >= self.blueprint.obsidian_ore and self.clay >= self.blueprint.obsidian_clay and (self.obsidian + self.obsidian_robots < self.blueprint.geode_obsidian):
                # make obsidian robot
                self.ore -= self.blueprint.obsidian_ore
                self.clay -= self.blueprint.obsidian_clay
                new_obsidian_robots += 1

            #while self.ore >= self.blueprint.clay_ore and (self.clay_robots / (self.obsidian_robots + 1) < self.blueprint.max_clay) and (self.clay_robots < self.blueprint.max_clay + 1):
            while self.ore >= self.blueprint.clay_ore and (self.clay + self.clay_robots < self.blueprint.obsidian_clay):
                # make clay robot
                self.ore -= self.blueprint.clay_ore
                new_clay_robots += 1

            while self.ore >= self.blueprint.ore and (not self.obsidian_robots):
                # make ore robot
                self.ore -= self.blueprint.ore
                new_ore_robots += 1

    def operate_with_priority(self, priorities: List):
        while self.minutes:
            new_geode_robots, new_obsidian_robots, new_clay_robots, new_ore_robots = 0, 0, 0, 0
            while self.ore >= self.blueprint.geode_ore and self.obsidian >= self.blueprint.geode_obsidian:
                # make geode robot
                self.ore -= self.blueprint.geode_ore
                self.obsidian -= self.blueprint.geode_obsidian
                new_geode_robots += 1

            priority = priorities[0]
            if priority == "obsidian" and self.ore >= self.blueprint.obsidian_ore and self.clay >= self.blueprint.obsidian_clay and (self.obsidian + self.obsidian_robots < self.blueprint.geode_obsidian):
                self.ore -= self.blueprint.obsidian_ore
                self.clay -= self.blueprint.obsidian_clay
                new_obsidian_robots += 1
                priorities.append(priorities.pop(0))

            elif priority == "clay" and self.ore >= self.blueprint.clay_ore:
                self.ore -= self.blueprint.clay_ore
                new_clay_robots += 1
                priorities.append(priorities.pop(0))

            elif priority == "ore" and self.ore >= self.blueprint.ore:
                self.ore -= self.blueprint.ore
                new_ore_robots += 1
                priorities.append(priorities.pop(0))

            # robots gather
            self.ore += self.ore_robots
            self.clay += self.clay_robots
            self.obsidian += self.obsidian_robots
            self.geodes_opened += self.geode_robots

            # robots finish building
            self.geode_robots += new_geode_robots
            self.obsidian_robots += new_obsidian_robots
            self.clay_robots += new_clay_robots
            self.ore_robots += new_ore_robots
            self.minutes -= 1

    def determine_quality_level(self):
        return self.blueprint.id * self.geodes_opened

    def __str__(self):
        return f"Factory(blueprint: {self.blueprint.id}), minute: {24 - self.minutes}\n  robots:\n - ore: {self.ore_robots}\n" \
               f" - clay: {self.clay_robots}\n - obsidian: {self.obsidian_robots}\n - geode: {self.geode_robots}\n" \
               f"  materials:\n - ore: {self.ore}\n - clay: {self.clay}\n - obsidian: {self.obsidian}\n - geode: {self.geodes_opened}\n"


if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=True, coerce=parse)
        print(f"{f.__name__}:\n\t{f(data)}")

