import re
from dataclasses import dataclass
from itertools import combinations_with_replacement, permutations, product
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
        levels = {}
        for build_order in product(["o", "c", "b"], repeat=14):
            if "c" not in build_order or "b" not in build_order:
                continue  # there's no way to crack geodes with obsidian which requires clay
            factory = Factory(blueprint)
            factory.operate_with_build_order(list(build_order))
            level = factory.determine_quality_level()
            levels[build_order] = level
        max_level = max(levels.values())
        print("Adding quality:", max_level)
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

    def operate_with_build_order(self, build_order):
        build_next = None
        while self.minutes:
            if not build_next:
                build_next = build_order.pop(0) if build_order else "b" # default to obsidian because why not
            new_geode_robots, new_obsidian_robots, new_clay_robots, new_ore_robots = 0, 0, 0, 0
            if self.ore >= self.blueprint.geode_ore and self.obsidian >= self.blueprint.geode_obsidian:
                # make geode robot
                self.ore -= self.blueprint.geode_ore
                self.obsidian -= self.blueprint.geode_obsidian
                new_geode_robots += 1

            if build_next == "b":
                if self.should_build_obsidian():
                    # make obsidian robot
                    self.ore -= self.blueprint.obsidian_ore
                    self.clay -= self.blueprint.obsidian_clay
                    new_obsidian_robots += 1
                    build_next = None

            elif build_next == "c":
                if self.ore >= self.blueprint.clay_ore:
                    # make clay robot
                    self.ore -= self.blueprint.clay_ore
                    new_clay_robots += 1
                    build_next = None
            elif build_next == "o":
                if self.ore >= self.blueprint.ore:
                    # make ore robot
                    self.ore -= self.blueprint.ore
                    new_ore_robots += 1
                    build_next = None

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

            #print(self)

    def operate_with_limits(self, max_clay_no_obsidian, max_clay):
        while self.minutes:
            # try to build, subtract resources
            new_geode_robots, new_obsidian_robots, new_clay_robots, new_ore_robots = 0, 0, 0, 0
            while self.ore >= self.blueprint.geode_ore and self.obsidian >= self.blueprint.geode_obsidian:
                # make geode robot
                self.ore -= self.blueprint.geode_ore
                self.obsidian -= self.blueprint.geode_obsidian
                new_geode_robots += 1

            while self.should_build_obsidian():
                # make obsidian robot
                self.ore -= self.blueprint.obsidian_ore
                self.clay -= self.blueprint.obsidian_clay
                new_obsidian_robots += 1

            while self.should_build_clay(max_clay_no_obsidian, max_clay):
                # make clay robot
                self.ore -= self.blueprint.clay_ore
                new_clay_robots += 1

            while self.ore >= self.blueprint.ore and (not self.obsidian_robots):
                # make ore robot
                self.ore -= self.blueprint.ore
                new_ore_robots += 1

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

            #print(self)

    def operate(self):
        while self.minutes:
            # try to build, subtract resources
            new_geode_robots, new_obsidian_robots, new_clay_robots, new_ore_robots = 0, 0, 0, 0
            while self.ore >= self.blueprint.geode_ore and self.obsidian >= self.blueprint.geode_obsidian:
                # make geode robot
                self.ore -= self.blueprint.geode_ore
                self.obsidian -= self.blueprint.geode_obsidian
                new_geode_robots += 1

            while self.should_build_obsidian():
                # make obsidian robot
                self.ore -= self.blueprint.obsidian_ore
                self.clay -= self.blueprint.obsidian_clay
                new_obsidian_robots += 1

            while self.should_build_clay():
                # make clay robot
                self.ore -= self.blueprint.clay_ore
                new_clay_robots += 1

            while self.ore >= self.blueprint.ore and (not self.obsidian_robots):
                # make ore robot
                self.ore -= self.blueprint.ore
                new_ore_robots += 1

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

            print(self)

    def determine_quality_level(self):
        return self.blueprint.id * self.geodes_opened

    def should_build_obsidian(self) -> bool:
        # we need to have the materials
        if self.ore < self.blueprint.obsidian_ore or self.clay < self.blueprint.obsidian_clay:
            return False

        ore_next_turn = self.ore + self.ore_robots
        obsidian_next_turn = self.obsidian + self.obsidian_robots

        # if there are no geode robots we need to build an obsidian one otherwise we'll never get the obsidian
        if not self.geode_robots:
            return True

        # only build obsidian robot if we couldn't build the geode robot next turn
        # because reasons
        return ore_next_turn < self.blueprint.geode_ore or obsidian_next_turn < self.blueprint.geode_obsidian

    def should_build_clay(self, max_clay_no_obsidian, max_clay):
        # we need to have the materials
        if self.ore < self.blueprint.clay_ore:
            return False

        # if there are no obsidian robots then we should build a clay robot otherwise we'll never get the clay
        if not self.obsidian_robots and self.clay_robots < max_clay_no_obsidian:
            return True

        return self.obsidian_robots and self.clay_robots < max_clay

        # if there are obsidian robots and we have the materials, only build if we couldn't build an obsidian robot
        # next turn because reasons
        #return self.ore + self.ore_robots < self.blueprint.obsidian_ore or self.clay + self.clay_robots < self.blueprint.obsidian_clay

    def __str__(self):
        return f"Factory(blueprint: {self.blueprint.id}), minute: {24 - self.minutes}\n  robots:\n - ore: {self.ore_robots}\n" \
               f" - clay: {self.clay_robots}\n - obsidian: {self.obsidian_robots}\n - geode: {self.geode_robots}\n" \
               f"  materials:\n - ore: {self.ore}\n - clay: {self.clay}\n - obsidian: {self.obsidian}\n - geode: {self.geodes_opened}\n"


# 810 is too low, 1016?, 1057, 1093 is too low
if __name__ == "__main__":
    for f in (part_one, part_two):
        data = get_input(__file__, is_sample=0, coerce=parse)
        print(f"{f.__name__}:\n\t{f(data)}")

