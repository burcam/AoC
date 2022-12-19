from dataclasses import dataclass
from enum import Enum
import functools
from math import floor
from statistics import mean
from typing import Dict, List, Sequence, Set, Tuple, TypeVar


with open("day18") as file:
    lines = []
    for line in file.readlines():
        line = line.strip().split(",")
        lines.append((int(line[0]), int(line[1]), int(line[2])))
lines.sort()
min_line = lines[0]
approx = 0
points: Set[Tuple] = set(lines)

@dataclass
class Lava():
    point: Tuple[int, int, int]
    direction: Tuple[int, int, int]

class Orientation(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    BACK = 4
    FRONT = 5
@dataclass(frozen=True)
class Side():
    point: Tuple[int, int, int]
    orientation: Orientation

checked_lava: Set[Lava] = set()
for line in lines:
    
    adding = 6
    if (line[0]-1, line[1], line[2]) in points:
        adding -=2
    if (line[0], line[1]-1, line[2]) in points:
        adding -=2
    if (line[0], line[1], line[2]-1) in points:
        adding -= 2
    points.add(line)
    #print(line, adding)
    approx += adding

lava = Lava(lines[0], (1,0,0))
found_sides: Set[Side] = set()
to_check = set([Side(lines[0], Orientation.LEFT)])

def side_check(side: Side, points: Set[Tuple]):
    muts1: List[Tuple]
    muts2: List[Tuple]
    match side.orientation:
        case Orientation.LEFT:
            muts1 = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0)]
            muts2 = [(-1, mut[1], mut[2]) for mut in muts1]
        case Orientation.RIGHT:
            muts1 = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0)]
            muts2 = [(1, mut[1], mut[2]) for mut in muts1]

        case Orientation.UP:
            muts1 = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
            muts2 = [(mut[0], mut[1], 1) for mut in muts1]
        case Orientation.DOWN:
            muts1 = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
            muts2 = [(mut[0], mut[1], -1) for mut in muts1]
        
        case Orientation.FRONT:
            muts1 = [(1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
            muts2 = [(mut[0], -1, mut[2]) for mut in muts1]
        case Orientation.BACK:
            muts1 = [(1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
            muts2 = [(mut[0], 1, mut[2]) for mut in muts1]
    sides = []
    for index, mut1 in enumerate(muts1):
        if tuple_sum(side.point, mut1) in points:
            if not tuple_sum(side.point, muts2[index]) in points:
                sides.append(Side(tuple_sum(side.point, mut1), side.orientation))
        if tuple_sum(side.point, muts2[index]) in points:
            orientation: Orientation
            if muts2[index][0] == -1:
                if side.orientation != Orientation.LEFT:
                    orientation = Orientation.RIGHT
                if muts2[index][1] == -1:
                    if side.orientation == Orientation.LEFT:
                        orientation = Orientation.BACK
                elif muts2[index][1] == 1:
                    if side.orientation == Orientation.LEFT:
                        orientation = Orientation.FRONT
                elif muts2[index][2] == 1:
                    if side.orientation == Orientation.LEFT:
                        orientation = Orientation.DOWN
                elif muts2[index][2] == -1:
                    if side.orientation == Orientation.LEFT:
                        orientation = Orientation.UP
            elif muts2[index][0] == 1:
                if side.orientation != Orientation.RIGHT:
                    orientation = Orientation.LEFT
                if muts2[index][1] == -1:
                    if side.orientation == Orientation.RIGHT:
                        orientation = Orientation.BACK
                elif muts2[index][1] == 1:
                    if side.orientation == Orientation.RIGHT:
                        orientation = Orientation.FRONT
                elif muts2[index][2] == 1:
                    if side.orientation == Orientation.RIGHT:
                        orientation = Orientation.DOWN
                elif muts2[index][2] == -1:
                    if side.orientation == Orientation.RIGHT:
                        orientation = Orientation.UP
            elif muts2[index][1] == -1:
                if side.orientation != Orientation.FRONT:
                    orientation = Orientation.BACK
                if muts2[index][2] == -1:
                    if side.orientation == Orientation.FRONT:
                        orientation = Orientation.UP
                elif muts2[index][2] == 1:
                    if side.orientation == Orientation.FRONT:
                        orientation = Orientation.DOWN
            elif muts2[index][1] == 1:
                if side.orientation != Orientation.BACK:
                    orientation = Orientation.FRONT
                if muts2[index][2] == -1:
                    if side.orientation == Orientation.BACK:
                        orientation = Orientation.UP
                elif muts2[index][2] == 1:
                    if side.orientation == Orientation.BACK:
                        orientation = Orientation.DOWN
            try:
                sides.append(Side(tuple_sum(side.point, muts2[index]), orientation))
            except Exception as ex:
                print(side, muts2[index])
                raise ex
        if not (tuple_sum(side.point, mut1) in points or tuple_sum(side.point, muts2[index]) in points):
            if mut1[0] == 1:
                orientation = Orientation.RIGHT
            elif mut1[0] == -1:
                orientation = Orientation.LEFT
            elif mut1[1] == 1:
                orientation = Orientation.BACK
            elif mut1[1] == -1:
                orientation = Orientation.FRONT
            elif mut1[2] == 1:
                orientation = Orientation.UP
            else:
                orientation = Orientation.DOWN
            sides.append(Side(side.point, orientation))
    return sides

def tuple_sum(t1: Tuple, t2: Tuple):
    ret = []
    for i in range(len(t1)):
        ret.append(t1[i]+t2[i])
    return tuple(ret)


while(len(to_check) > 0):
    side = to_check.pop()
    found_sides.add(side)
    next_sides = side_check(side, points)
    to_check.update([side for side in next_sides if side not in found_sides])

print(len(found_sides))