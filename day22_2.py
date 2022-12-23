from dataclasses import dataclass
from enum import Enum
import functools
from math import ceil
import re
import time
from typing import Dict, List, Set, Tuple

class Direction(Enum):
    R = 0
    D = 1
    L = 2
    U = 3

@dataclass
class Location():
    row: int
    column: int
    left: 'Location'|Tuple[int, int]
    left_dir: Direction
    right: 'Location'|Tuple[int, int]
    right_dir: Direction
    up: 'Location'|Tuple[int, int]
    up_dir: Direction
    down: 'Location'|Tuple[int, int]
    down_dir: Direction
    is_wall: bool

commands = []
locations: Dict[Tuple[int, int], Location] = {}
path_mark = False
current: Location = None
with open("day22") as file:
    lines = file.readlines()
for f_index, line in enumerate(lines):
    line = line.strip("\n")
    if line == "":
        path_mark = True
    elif path_mark:
        break
    else:
        for index, char in enumerate(line):
            left, left_dir =   (f_index, index - 1), Direction.L
            up, up_dir =       (f_index-1, index), Direction.U
            down, down_dir =   (f_index+1, index), Direction.D
            right, right_dir = (f_index, index + 1), Direction.R
            if f_index < 50:
                if index < 50:
                    continue
                elif index == 50:
                    left = (149-f_index, 0)
                    left_dir = Direction.R
                elif index == 149:
                    right = (149-f_index, 99)
                    right_dir = Direction.L
                
                if f_index == 0 and index < 100:
                    up = (100+index, 0)
                    up_dir = Direction.R
                elif f_index == 0 and index > 99:
                    up = (199, index-100)
                    up_dir = Direction.U
                elif f_index == 49:
                    if index > 99:
                        down = (index-50, 99)
                        down_dir = Direction.L

            elif f_index < 100:
                if index < 50:
                    continue
                elif index == 50:
                    left = (100, f_index-50)
                    left_dir = Direction.D
                elif index == 99:
                    right = (49, f_index+50)
                    right_dir = Direction.U
            
            elif f_index < 150:
                if f_index == 100:
                    if index < 50:
                        up = (50+index, 50)
                        up_dir = Direction.R
                if index == 0:
                    left = (149-f_index, 50)
                    left_dir = Direction.R
                elif index == 99:
                    right = (149-f_index, 149)
                    right_dir = Direction.L
                
                if f_index == 149 and index > 49:
                    down = (100+index, 49)
                    down_dir = Direction.L
            
            else:
                if index == 0:
                    left = (0, f_index - 100)
                    left_dir = Direction.D
                if index == 49:
                    right = (149, f_index-100)
                    right_dir = Direction.U
                if f_index == 199:
                    down = (0, index+100)
                    down_dir = Direction.D

            cur_lock = Location(f_index, index, left, left_dir, right, right_dir, up, up_dir, down, down_dir, char == "#")
            if current is None:
                current = cur_lock
            locations.setdefault((f_index, index), cur_lock)

for location in locations.values():
    print(location.row, location.column)
    test = locations[location.up]
    if test.is_wall:
        location.up_dir = Direction.U
        location.up = location
    else:
        location.up = test
    
    test = locations[location.left]
    if test.is_wall:
        location.left_dir = Direction.L
        location.left = location
    else:
        location.left = test
    
    test = locations[location.right]
    if test.is_wall:
        location.right_dir = Direction.R
        location.right = location
    else:
        location.right = test
    
    test = locations[location.down]
    if test.is_wall:
        location.down_dir = Direction.D
        location.down = location
    else:
        location.down = test

# print(walls)
# for location in locations.values():
#     print((location.row, location.column))
#     print("  ", (location.up.row, location.up.column))
#     print("  ", (location.left.row, location.left.column))
#     print("  ", (location.right.row, location.right.column))
#     print("  ", (location.down.row, location.down.column))
direction = Direction.R
def new_direction(direction: Direction, command: str):
    if direction == Direction.R:
        if command == "R":
            return Direction.D
        return Direction.U
    if direction == Direction.D:
        if command == "R":
            return Direction.L
        return Direction.R
    if direction == Direction.L:
        if command == "R":
            return Direction.U
        return Direction.D
    if command == "R":
        return Direction.R
    return Direction.L
while len(line) > 0:
    command = line[0]
    if command == "R" or command == "L":
        direction = new_direction(direction, command)
        line = line[1:]
    else:
        command = int(re.match("^[0-9]+", line).group(0))
        for _ in range(command):
            if direction == Direction.U:
                direction = current.up_dir
                current = current.up
            elif direction == Direction.D:
                direction = current.down_dir
                current = current.down
            elif direction == Direction.L:
                direction = current.left_dir
                current = current.left
            elif direction == Direction.R:
                direction = current.right_dir
                current = current.right
        line = line[len(str(command)):]
print(current.row+1, current.column+1, direction)
if direction == Direction.R:
    facing = 0
if direction == Direction.D:
    facing = 1
if direction == Direction.L:
    facing = 2
if direction == Direction.U:
    facing = 3
print((current.row+1)*1000 + (current.column+1)*4 + facing)
#7548 - Low
#58277 - Low
#184163- High
#179091