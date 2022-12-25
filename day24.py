from dataclasses import dataclass
from enum import Enum
import functools
from math import ceil
from queue import Queue
import re
import time
from typing import Dict, List, Set, Tuple

class Direction(Enum):
    UP = '^'
    LEFT = '<'
    RIGHT = '>'
    DOWN = 'v'

@dataclass
class Point():
    def __hash__(self) -> int:
        return (self.row, self.column).__hash__()
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Point) and self.row == __o.row and self.column == __o.column
    row: int
    column: int
    def move(self, grid: Dict[Tuple[int, int], List['Point']]):
        pass
@dataclass
class Wall(Point):
    def move(self, grid: Dict[Tuple[int, int], List[Point]]):
        return (self.row, self.column)

class Expedition(Point):
    def move(self, grid: Dict[Tuple[int, int], List[Point]]):
        pass
class End(Point):
    def move(self, grid: Dict[Tuple[int, int], List[Point]]):
        pass
@dataclass
class Blizzard(Point):
    direction: Direction
    def move(self, grid: Dict[Tuple[int, int], List[Point]]):
        if self.direction == Direction.UP:
            next_loc = (self.row - 1, self.column)
        elif self.direction == Direction.DOWN:
            next_loc = (self.row + 1, self.column)
        elif self.direction == Direction.LEFT:
            next_loc = (self.row, self.column - 1)
        else:
            next_loc = (self.row, self.column + 1)
        if next_loc in grid.keys() and isinstance(grid[next_loc][0], Wall):
            if self.direction == Direction.UP:
                next_loc = (len(lines)-2, self.column)
            elif self.direction == Direction.DOWN:
                next_loc = (1, self.column)
            elif self.direction == Direction.LEFT:
                next_loc = (self.row, len(line)-2)
            else:
                next_loc = (self.row, 1)
        return next_loc


grid: Dict[Tuple[int, int], List[Point]] = {}

with open("day24") as file:
    lines = file.readlines()
for row, line in enumerate(lines):
    line = line.strip("\n")
    for col, char in enumerate(line):
        if row == 0:
            if char == ".":
                exp = Expedition(row, col)
                continue
        if row == len(lines) - 1:
            if char == ".":
                end = End(row, col)
                continue
        if char == ".":
            continue
        if char == "#":
            grid[(row, col)] = [Wall(row, col)]
            continue
        grid[(row, col)] = [Blizzard(row, col, Direction(char))]

def print_grid(grid: Dict[Tuple[int, int], List[Point]]):
    keys = grid.keys()
    for row in range(len(lines)):
        print_line = ""
        for col in range(len(line)):
            if (row, col) not in keys:
                print_line += "."
            else:
                if isinstance(grid[(row, col)][0], Wall):
                    print_line += "#"
                elif len(grid[(row, col)]) == 1:
                    print_line += grid[(row, col)][0].direction.value
                else:
                    print_line += str(len(grid[(row, col)]))
        print(print_line)
    print("")

@functools.cache
def move_blizzards(round: int) -> Dict[Tuple[int, int], List[Point]]:
    if round == 0:
        return grid
    prev_grid = move_blizzards(round-1)
    next_grid: Dict[Tuple[int, int], List[Point]] = {}
    for items in prev_grid.values():
        for item in items:
            if isinstance(item, Blizzard):
                move = item.move(prev_grid)
                next_bliz = Blizzard(move[0], move[1], item.direction)
                if (move[0], move[1]) in next_grid.keys():
                    next_grid[(move[0], move[1])].append(next_bliz)
                else:
                    next_grid[(move[0], move[1])] = [next_bliz]
                continue
            next_grid[(item.row, item.column)] = [item]
    return next_grid


def next_exps(expedition: Point, round: int):
    if expedition.row == end.row and expedition.column == end.column:
        return 0
    next_grid = move_blizzards(round+1)
    blocked_keys = next_grid.keys()
    to_check = []
    if expedition.row > 0:
        if (expedition.row - 1, expedition.column) not in blocked_keys:
            to_check.append((expedition.row - 1, expedition.column))
    if expedition.row < len(lines)-1:
        if (expedition.row + 1, expedition.column) not in blocked_keys:
            to_check.append((expedition.row + 1, expedition.column))
    if (expedition.row, expedition.column - 1) not in blocked_keys:
        to_check.append((expedition.row, expedition.column - 1))
    if (expedition.row, expedition.column + 1) not in blocked_keys:
        to_check.append((expedition.row, expedition.column + 1))
    if (expedition.row, expedition.column) not in blocked_keys:
        to_check.append((expedition.row, expedition.column))
    return to_check

round = 0
exp_locations: Set[Tuple[int, Point]] = set()
exp_locations.add((0, exp))

print_grid(grid)
low = 259
high = 1_000_000
while(len(exp_locations) > 0):
    curr_exp = exp_locations.pop()
    next_exp = next_exps(curr_exp[1], curr_exp[0])
    if next_exp == 0:
        high = min(curr_exp[0], high)
        continue
    for val in next_exp:
        if curr_exp[0]+1 < high:
            exp_locations.add((curr_exp[0]+1, Point(val[0], val[1])))

high1 = 1_000_000
exp, end = end, exp
exp_locations: Set[Tuple[int, Point]] = set()
exp_locations.add((high, exp))

while(len(exp_locations) > 0):
    curr_exp = exp_locations.pop()
    next_exp = next_exps(curr_exp[1], curr_exp[0])
    if next_exp == 0:
        high1 = min(curr_exp[0], high1)
        continue
    for val in next_exp:
        if curr_exp[0]+1 < high1:
            exp_locations.add((curr_exp[0]+1, Point(val[0], val[1])))

high2 = 1_000_000
exp, end = end, exp
exp_locations: Set[Tuple[int, Point]] = set()
exp_locations.add((high1, exp))

while(len(exp_locations) > 0):
    curr_exp = exp_locations.pop()
    next_exp = next_exps(curr_exp[1], curr_exp[0])
    if next_exp == 0:
        high2 = min(curr_exp[0], high2)
        continue
    for val in next_exp:
        if curr_exp[0]+1 < high2:
            exp_locations.add((curr_exp[0]+1, Point(val[0], val[1])))
print(high2)

#277 - high