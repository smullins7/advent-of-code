import math
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple

from utils.inputs import get_input

PARSE_PAT = re.compile(
    r"Blueprint (?P<id>\d+): Each ore robot costs (?P<ore>\d+) ore. Each clay robot costs (?P<clay_ore>\d+) ore. Each obsidian robot costs (?P<obsidian_ore>\d+) ore and (?P<obsidian_clay>\d+) clay. Each geode robot costs (?P<geode_ore>\d+) ore and (?P<geode_obsidian>\d+) obsidian.")


def parse(line):
    return Blueprint(
        **{k: int(v) for k, v in PARSE_PAT.match(line).groupdict().items()}
    )


@dataclass
class Blueprint:
    id: int
    ore: int
    clay_ore: int
    obsidian_ore: int
    obsidian_clay: int
    geode_ore: int
    geode_obsidian: int

    def get_max_clay_robots(self):
        return self.obsidian_clay

    def get_max_obsidian_robots(self):
        return self.geode_obsidian

    def get_max_ore_robots(self):
        return max(self.obsidian_ore, self.geode_ore)


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

    def take_turn(self):
        new_factories = []
        bots_to_build = self.determine_possible_builds()
        for robot_to_build in bots_to_build:
            factory = Factory.copy_from(self)
            factory.gather_materials()
            factory.build_robot(robot_to_build)
            new_factories.append(factory)

        if "geode" not in bots_to_build and "obsidian" not in bots_to_build:
            # we did not build a geode or obsidian robot, so an option is to just gather this turn
            new_factories.append(self)
            self.gather_materials()

        return new_factories

    def determine_possible_builds(self) -> List[str]:
        # last turn, no point in building anything, just gather
        if self.minutes == 1:
            return []
        # building a geode robot always takes priority, consider no other action
        if self.can_build("geode"):
            return ["geode"]
        # if this is the last useful turn to build, and I can't build a geode then don't bother building anything
        if self.minutes == 2 and (
                self.ore + self.ore_robots < self.blueprint.geode_ore or self.obsidian + self.obsidian_robots < self.blueprint.geode_obsidian):
            return []
        # if this is the last useful turn to an obsidian, and building one won't let me build a geode next turn then don't bother building anything
        if self.minutes == 3 and (self.obsidian + self.obsidian_robots + 1 < self.blueprint.geode_obsidian):
            return []
        # prioritize obsidian over clay and ore since it's critical for geode
        if self.can_build("obsidian"):
            return ["obsidian"]

        return [r for r in ("clay", "ore") if self.can_build(r)]

    def gather_materials(self):
        self.ore += self.ore_robots
        self.clay += self.clay_robots
        self.obsidian += self.obsidian_robots
        self.geodes_opened += self.geode_robots

        self.minutes -= 1

    def build_robot(self, robot: str):
        if robot == "geode":
            self.ore -= self.blueprint.geode_ore
            self.obsidian -= self.blueprint.geode_obsidian
            self.geode_robots += 1
        elif robot == "obsidian":
            self.ore -= self.blueprint.obsidian_ore
            self.clay -= self.blueprint.obsidian_clay
            self.obsidian_robots += 1
        elif robot == "clay":
            self.ore -= self.blueprint.clay_ore
            self.clay_robots += 1
        else:  # ore
            self.ore -= self.blueprint.ore
            self.ore_robots += 1

        if self.ore < 0 or self.clay < 0 or self.obsidian < 0:
            print("bug here", self)

    def can_build(self, robot: str):
        if robot == "geode":
            return self.ore >= self.blueprint.geode_ore and self.obsidian >= self.blueprint.geode_obsidian
        elif robot == "obsidian":
            return self.ore >= self.blueprint.obsidian_ore and self.clay >= self.blueprint.obsidian_clay  # and self.obsidian_robots < self.blueprint.get_max_obsidian_robots()
        elif robot == "clay":
            return self.ore >= self.blueprint.clay_ore and self.clay_robots < self.blueprint.get_max_clay_robots()
        else:  # ore
            return self.ore >= self.blueprint.ore and self.ore_robots < self.blueprint.get_max_ore_robots()

    def operate_with_build_order(self, build_order):
        build_next = None
        while self.minutes:
            if not build_next:
                build_next = build_order.pop(0) if build_order else "b"  # default to obsidian because why not
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

            # print(self)

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

            # print(self)

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
        # return self.ore + self.ore_robots < self.blueprint.obsidian_ore or self.clay + self.clay_robots < self.blueprint.obsidian_clay

    @staticmethod
    def copy_from(other):
        return Factory(
            other.blueprint,
            other.minutes,
            other.ore,
            other.ore_robots,
            other.clay,
            other.clay_robots,
            other.obsidian,
            other.obsidian_robots,
            other.geode_robots,
            other.geodes_opened,
        )

    def __str__(self):
        return f"Factory(blueprint: {self.blueprint.id}), minute: {24 - self.minutes}\n  robots:\n - ore: {self.ore_robots}\n" \
               f" - clay: {self.clay_robots}\n - obsidian: {self.obsidian_robots}\n - geode: {self.geode_robots}\n" \
               f"  materials:\n - ore: {self.ore}\n - clay: {self.clay}\n - obsidian: {self.obsidian}\n - geode: {self.geodes_opened}\n"


def part_one(blueprints: List[Blueprint]):
    quality_levels = []
    for blueprint in blueprints:
        print("Checking blueprint", blueprint.id)

        blueprint_best_quality_level = geodes_for_bp(blueprint, 24) * blueprint.id
        print(blueprint.id, "quality level", blueprint_best_quality_level, "score",
              blueprint_best_quality_level / blueprint.id)
        quality_levels.append(blueprint_best_quality_level)

    return sum(quality_levels)


def part_two(blueprints: List[Blueprint]):
    scores = []
    for blueprint in blueprints[:3]:
        print("Checking blueprint", blueprint.id)
        geodes = geodes_for_bp(blueprint, 32)
        print(blueprint.id, "score", geodes)
        scores.append(geodes)

    return math.prod(scores)


def can_build(bp: Blueprint, robots: Tuple, mats: Tuple, robot):
    if robot == "geode":
        return mats[0] >= bp.geode_ore and mats[2] >= bp.geode_obsidian
    elif robot == "obsidian":
        return mats[0] >= bp.obsidian_ore and mats[1] >= bp.obsidian_clay and robots[2] < bp.get_max_obsidian_robots()
    elif robot == "clay":
        return mats[0] >= bp.clay_ore and robots[1] < bp.get_max_clay_robots()
    else:  # ore
        return mats[0] >= bp.ore and robots[0] < bp.get_max_ore_robots()


def determine_builds(bp: Blueprint, minutes: int, robots: Tuple, mats: Tuple):
    if minutes == 1:
        return []
    # building a geode robot always takes priority, consider no other action
    if can_build(bp, robots, mats, "geode"):
        return ["geode"]
    # if this is the last useful turn to build, and I can't build a geode then don't bother building anything
    if minutes == 2 and (
            robots[0] + mats[0] < bp.geode_ore or robots[2] + mats[2] < bp.geode_obsidian):
        return []
    # if this is the last useful turn to an obsidian, and building one won't let me build a geode next turn then don't bother building anything
    #if minutes == 3 and (robots[2] + mats[2] + 1 < bp.geode_obsidian):
    #    return []
    # prioritize obsidian over clay and ore since it's critical for geode
    #if can_build(bp, robots, mats, "obsidian"):
    #    return ["obsidian"]

    return [r for r in ("clay", "ore", "obsidian") if can_build(bp, robots, mats, r)]


def gather_resources(robots, mats):
    return tuple([l + r for l, r in zip(robots, mats)])


def build(bp: Blueprint, robots: Tuple, mats: Tuple, robot) -> Tuple:
    # bp, min, ore r, clay r, ob r,  geode r, ore, clay, obs, geode)
    new_ore, new_clay, new_obs, new_geode = 0, 0, 0, 0
    less_ore, less_clay, less_obs = 0, 0, 0
    if robot == "geode":
        new_geode = 1
        less_ore = bp.geode_ore
        less_obs = bp.geode_obsidian
    elif robot == "obsidian":
        new_obs = 1
        less_ore = bp.obsidian_ore
        less_clay = bp.obsidian_clay
    elif robot == "clay":
        new_clay = 1
        less_ore = bp.clay_ore
    else:  # ore
        new_ore = 1
        less_ore = bp.ore

    return (
        (robots[0] + new_ore, robots[1] + new_clay, robots[2] + new_obs, robots[3] + new_geode),
        (mats[0] - less_ore, mats[1] - less_clay, mats[2] - less_obs, mats[3])
    )


def do(bp: Blueprint, minutes: int, robots: Tuple, mats: Tuple) -> List:
    new_things = []
    to_build = determine_builds(bp, minutes, robots, mats)
    for robot_to_build in to_build:
        updated_robots, updated_mats = build(bp, robots, mats, robot_to_build)
        if any(map(lambda n: n < 0, updated_mats)):
            raise ValueError(f"negative resources is bug: {updated_robots}, {updated_mats}, {robot_to_build}")
        new_things.append((minutes - 1, updated_robots, gather_resources(robots, updated_mats)))

    if "geode" not in to_build:# and "obsidian" not in to_build:
        # we did not build a geode or obsidian robot, so an option is to just gather this turn
        new_things.append((minutes - 1, robots, gather_resources(robots, mats)))

    return new_things


def geodes_for_bp(blueprint: Blueprint, minutes):
    q = [
        # queue for the current minute
        [
            # min, robots, mats
            (minutes, (1, 0, 0, 0), (0, 0, 0, 0))
        ]
    ]

    best = 0
    while q:
        current_minute_to_check = q.pop(0)
        next_minute = []

        for minutes, robots, mats in current_minute_to_check:
            geodes = mats[-1]
            if not minutes:
                best = max(best, geodes)
            else:
                for _next in do(blueprint, minutes, robots, mats):
                    next_minute.append(_next)

        if next_minute:
            # only consider the paths where we've opened the most geodes so far, as all other paths
            # will never catch up
            best_this_minute = max(_next[2][3] for _next in next_minute)
            q.append([_next for _next in next_minute if _next[2][3] - 1 <= best_this_minute])

    return best


# 810 is too low, 1016?, 1057, 1093 is too low
if __name__ == "__main__":
    for f in (part_two,):
        data = get_input(__file__, is_sample=1, coerce=parse)
        print(f"{f.__name__}:\n\t{f(data)}")
