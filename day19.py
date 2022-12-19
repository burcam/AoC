from dataclasses import dataclass
from enum import Enum
import functools
from math import ceil
import re
import time
from typing import Dict, List, Set, Tuple

minutes = 24
#Blueprint 4: Each ore robot costs 4 ore. Each clay robot costs 3 ore. Each obsidian robot costs 4 ore and 18 clay. Each geode robot costs 4 ore and 11 obsidian.
@dataclass(frozen=True)
class Blueprint():
    blueprint_num: int
    ore_robot_cost: int
    clay_robot_cost: int
    obsidian_robot_cost: Tuple[int, int]
    geode_robot_cost: Tuple[int, int]
    previous_attempt: int
    def print(self):
        print(f"Blueprint {self.blueprint_num}:")
        print(f"  Each ore robot costs {self.ore_robot_cost} ore.")
        print(f"  Each clay robot costs {self.clay_robot_cost} ore.")
        print(f"  Each obsidian robot costs {self.obsidian_robot_cost[0]} ore and {self.obsidian_robot_cost[1]} clay.")
        print(f"  Each geode robot costs {self.geode_robot_cost[0]} ore and {self.geode_robot_cost[1]} obsidian.")

blueprints: List[Blueprint] = []

with open("day19_2") as file:
    for line in file.readlines():
        line = line.strip()
        matches = re.match("Blueprint (.*): Each ore robot costs (.*) ore. Each clay robot costs (.*) ore. Each obsidian robot costs (.*) ore and (.*) clay. Each geode robot costs (.*) ore and (.*) obsidian.(.*)$", line).groups()
        blueprints.append(Blueprint(
            int(matches[0]),
            int(matches[1]),
            int(matches[2]),
            (int(matches[3]), int(matches[4])),
            (int(matches[5]), int(matches[6])),
            int(matches[7] or -1)))

class Bots(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3
    HOLD_GEO = 4
    HOLD_OBS = 5
    HOLD_CLA = 6
    HOLD_ORE = 7

def ore_time_required(blueprint: Blueprint, ore_bots: int, ore: int):
    if ore >= blueprint.ore_robot_cost:
        return 0
    return ceil((blueprint.ore_robot_cost - ore)/ore_bots)

def clay_time_required(blueprint: Blueprint, ore_bots: int, ore: int):
    if ore >= blueprint.clay_robot_cost:
        return 0
    return ceil((blueprint.clay_robot_cost - ore)/ore_bots)

def obsidian_time_required(blueprint: Blueprint, ore_bots: int, ore: int, clay_bots: int, clay: int):
    if ore >= blueprint.obsidian_robot_cost[0] and clay >= blueprint.obsidian_robot_cost[1]:
        return 0
    if clay_bots == 0:
        return 30
    return max(ceil((blueprint.obsidian_robot_cost[0] - ore)/ore_bots), ceil((blueprint.obsidian_robot_cost[1] - clay)/clay_bots))

def geode_time_required(blueprint: Blueprint, ore_bots: int, ore: int, obsidian_bots: int, obsidian: int):
    if ore >= blueprint.geode_robot_cost[0] and obsidian >= blueprint.geode_robot_cost[1]:
        return 0
    if obsidian_bots == 0:
        return 30
    return max(ceil((blueprint.geode_robot_cost[0] - ore)/ore_bots), ceil((blueprint.geode_robot_cost[1] - obsidian)/obsidian_bots))

def target_bot(blueprint: Blueprint, ore_bots: int, clay_bots: int, obsidian_bots: int, ore: int, clay: int, obsidian: int):
    geode_time = geode_time_required(blueprint, ore_bots, ore, obsidian_bots, obsidian)
    if geode_time == 0:
        return Bots.GEODE
    obsidian_time = obsidian_time_required(blueprint, ore_bots, ore, clay_bots, clay)
    ore_time = ore_time_required(blueprint, ore_bots, ore)
    if geode_time <= obsidian_time and geode_time <= ore_time:
        return Bots.HOLD_GEO
    if geode_time < obsidian_time + geode_time_required(blueprint, ore_bots, ore-blueprint.obsidian_robot_cost[0], obsidian_bots+1, obsidian):
        return Bots.HOLD_GEO
    clay_time = clay_time_required(blueprint, ore_bots, ore)


def geode_count(blueprint: Blueprint, minutes_left: int, ore_bots: int, clay_bots: int, obsidian_bots: int, ore: int, clay: int, obsidian: int):
    if minutes_left < 1:
        return 0
    max_geodes = 0
    if ore >= blueprint.geode_robot_cost[0] and obsidian >= blueprint.geode_robot_cost[1]:
        print(ore_bots, clay_bots, obsidian_bots, blueprint.geode_robot_cost)
        return (minutes_left - 1) + geode_count(blueprint, minutes_left - 1,
            ore_bots, clay_bots, obsidian_bots,
            ore - blueprint.geode_robot_cost[0] + ore_bots,
            clay + clay_bots,
            obsidian - blueprint.geode_robot_cost[1] + obsidian_bots)
    if ore >= blueprint.obsidian_robot_cost[0] and clay >= blueprint.obsidian_robot_cost[1]:
        temp = geode_count(blueprint, minutes_left - 1,
            ore_bots, clay_bots, obsidian_bots + 1,
            ore - blueprint.obsidian_robot_cost[0] + ore_bots,
            clay - blueprint.obsidian_robot_cost[1] + clay_bots,
            obsidian + obsidian_bots)
        if temp > max_geodes:
            max_geodes = temp
    if ore >= blueprint.clay_robot_cost:
        temp = geode_count(blueprint, minutes_left - 1,
            ore_bots, clay_bots + 1, obsidian_bots ,
            ore - blueprint.clay_robot_cost + ore_bots,
            clay + clay_bots,
            obsidian + obsidian_bots)
        if temp > max_geodes:
            max_geodes = temp
    if ore >= blueprint.ore_robot_cost:
        temp = geode_count(blueprint, minutes_left - 1,
            ore_bots + 1, clay_bots, obsidian_bots ,
            ore - blueprint.ore_robot_cost + ore_bots,
            clay + clay_bots,
            obsidian + obsidian_bots)
        if temp > max_geodes:
            max_geodes = temp
    
    temp = geode_count(blueprint, minutes_left - 1,
        ore_bots , clay_bots, obsidian_bots ,
        ore + ore_bots,
        clay + clay_bots,
        obsidian + obsidian_bots)
    if temp > max_geodes:
        max_geodes = temp
    return max_geodes
    
blueprint_qualities: List[int] = []
for blueprint in blueprints:
    quality = geode_count(blueprint, 32, 1, 0, 0, 0, 0, 0) if blueprint.previous_attempt == -1 else blueprint.previous_attempt
    print(blueprint.blueprint_num, quality)
    blueprint_qualities.append(quality)
print(blueprint_qualities[0]* blueprint_qualities[1] * blueprint_qualities[2])