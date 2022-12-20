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

@dataclass(frozen=True)
class Step():
    blueprint: Blueprint
    ore: int
    clay: int
    obsidian: int
    ore_bots: int
    clay_bots: int
    obsidian_bots: int
    def next_ore(self):
        if self.ore_bots == max(self.blueprint.clay_robot_cost, self.blueprint.obsidian_robot_cost[0], self.blueprint.geode_robot_cost[0]):
            return -1
        if self.blueprint.ore_robot_cost <= self.ore:
            return 0
        return ceil((self.blueprint.ore_robot_cost - self.ore)/self.ore_bots)
    def next_clay(self):
        if self.clay_bots == self.blueprint.obsidian_robot_cost[1]:
            return -1
        if self.blueprint.clay_robot_cost <= self.ore:
            return 0
        return ceil((self.blueprint.clay_robot_cost - self.ore)/self.ore_bots)
    def next_obsidian(self):
        if self.clay_bots == 0 or self.obsidian_bots == self.blueprint.geode_robot_cost[1]:
            return -1
        if self.blueprint.obsidian_robot_cost[0] <= self.ore and self.blueprint.obsidian_robot_cost[1] <= self.clay:
            return 0
        return max(
            ceil((self.blueprint.obsidian_robot_cost[0]-self.ore)/self.ore_bots),
            ceil((self.blueprint.obsidian_robot_cost[1]-self.clay)/self.clay_bots),
            )
    def next_geode(self):
        if self.obsidian_bots == 0:
            return -1
        if self.blueprint.geode_robot_cost[0] <= self.ore and self.blueprint.geode_robot_cost[1] <= self.obsidian:
            return 0
        return max(
            ceil((self.blueprint.geode_robot_cost[0]-self.ore)/self.ore_bots),
            ceil((self.blueprint.geode_robot_cost[1]-self.obsidian)/self.obsidian_bots),
            )
    def ore_step(self, inc: int):
        return Step(
            self.blueprint,
            self.ore+self.ore_bots*inc-self.blueprint.ore_robot_cost,
            self.clay+self.clay_bots*inc,
            self.obsidian+self.obsidian_bots*inc,
            self.ore_bots+1,
            self.clay_bots,
            self.obsidian_bots
        )
    def clay_step(self, inc: int):
        return Step(
            self.blueprint,
            self.ore+self.ore_bots*inc-self.blueprint.clay_robot_cost,
            self.clay+self.clay_bots*inc,
            self.obsidian+self.obsidian_bots*inc,
            self.ore_bots,
            self.clay_bots+1,
            self.obsidian_bots
        )
    def obsidian_step(self, inc: int):
        return Step(
            self.blueprint,
            self.ore+self.ore_bots*inc-self.blueprint.obsidian_robot_cost[0],
            self.clay+self.clay_bots*inc-self.blueprint.obsidian_robot_cost[1],
            self.obsidian+self.obsidian_bots*inc,
            self.ore_bots,
            self.clay_bots,
            self.obsidian_bots+1
        )
    def geode_step(self, inc: int):
        return Step(
            self.blueprint,
            self.ore+self.ore_bots*inc-self.blueprint.geode_robot_cost[0],
            self.clay+self.clay_bots*inc,
            self.obsidian+self.obsidian_bots*inc-self.blueprint.geode_robot_cost[1],
            self.ore_bots,
            self.clay_bots,
            self.obsidian_bots
        )

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


def geode_count(minutes_left: int, step: Step):
    
    if minutes_left < 1:
        return 0
    jumps = [step.next_geode(), step.next_obsidian(), step.next_clay(), step.next_ore()]
    counts = [0]
    if jumps[0] != -1 and (minutes_left-jumps[0]-1) > 0:
        counts.append(geode_count(minutes_left-jumps[0]-1, step.geode_step(jumps[0]+1)) + minutes_left-jumps[0]-1)
    if jumps[1] != -1:
        counts.append(geode_count(minutes_left-jumps[1]-1, step.obsidian_step(jumps[1]+1)))
    if jumps[2] != -1:
        counts.append(geode_count(minutes_left-jumps[2]-1, step.clay_step(jumps[2]+1)))
    if jumps[3] != -1:
        counts.append(geode_count(minutes_left-jumps[3]-1, step.ore_step(jumps[3]+1)))
    if len(counts) == 1:
        return counts[0]
    return max(*counts)
    
blueprint_qualities: List[int] = []
for blueprint in blueprints:
    step = Step(blueprint, 0, 0, 0, 1, 0, 0)
    quality = geode_count(32, step) if blueprint.previous_attempt == -1 else blueprint.previous_attempt
    print(blueprint.blueprint_num, quality)
    blueprint_qualities.append(quality)
print(blueprint_qualities[0]* blueprint_qualities[1] * blueprint_qualities[2])