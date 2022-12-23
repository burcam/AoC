from dataclasses import dataclass
from enum import Enum
import functools
from math import ceil
import re
import time
from typing import Dict, List, Set, Tuple

@dataclass
class Location():
    row: int
    column: int
    left: 'Location'
    right: 'Location'
    up: 'Location'
    down: 'Location'

commands = []
locations: Dict[Tuple[int, int], Location] = {}
walls: List[Tuple[int, int]] = []
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
            if char == " ":
                continue
            if char == "#":
                walls.append((f_index, index))
                continue
            cur_lock = Location(f_index, index, None, None, None, None)
            if current is None:
                current = cur_lock
            locations.setdefault((f_index, index), cur_lock)

loc_keys = locations.keys()
for lock in locations.values():
    if (lock.row-1, lock.column) in walls:
        lock.up = lock
    elif (lock.row-1, lock.column) in loc_keys:
        lock.up = locations[(lock.row-1, lock.column)]
    else:
        inc = 0
        while True:
            if (lock.row+inc, lock.column) not in walls and (lock.row+inc, lock.column) not in loc_keys:
                if (lock.row+inc - 1, lock.column) in walls:
                    lock.up = lock
                else:
                    lock.up = locations[(lock.row+inc - 1, lock.column)]
                break
            inc += 1
    
    if (lock.row, lock.column-1) in walls:
        lock.left = lock
    elif (lock.row, lock.column-1) in loc_keys:
        lock.left = locations[(lock.row, lock.column-1)]
    else:
        inc = 0
        while True:
            if (lock.row, lock.column+inc) not in walls and (lock.row, lock.column+inc) not in loc_keys:
                if (lock.row, lock.column+inc - 1) in walls:
                    lock.left = lock
                else:
                    lock.left = locations[(lock.row, lock.column+inc - 1)]
                break
            inc += 1
    
    if (lock.row+1, lock.column) in walls:
        lock.down = lock
    elif (lock.row+1, lock.column) in loc_keys:
        lock.down = locations[(lock.row+1, lock.column)]
    else:
        inc = 0
        while True:
            if (lock.row-inc, lock.column) not in walls and (lock.row-inc, lock.column) not in loc_keys:
                if (lock.row-inc + 1, lock.column) in walls:
                    lock.down = lock
                else:
                    lock.down = locations[(lock.row-inc + 1, lock.column)]
                break
            inc += 1
    
    if (lock.row, lock.column+1) in walls:
        lock.right = lock
    elif (lock.row, lock.column+1) in loc_keys:
        lock.right = locations[(lock.row, lock.column+1)]
    else:
        inc = 0
        while True:
            if (lock.row, lock.column-inc) not in walls and (lock.row, lock.column-inc) not in loc_keys:
                if (lock.row, lock.column-inc + 1) in walls:
                    lock.right = lock
                else:
                    lock.right = locations[(lock.row, lock.column-inc + 1)]
                break
            inc += 1

# print(walls)
# for location in locations.values():
#     print((location.row, location.column))
#     print("  ", (location.up.row, location.up.column))
#     print("  ", (location.left.row, location.left.column))
#     print("  ", (location.right.row, location.right.column))
#     print("  ", (location.down.row, location.down.column))
direction = "R"
def new_direction(direction: str, command: str):
    if direction == "R":
        if command == "R":
            return "D"
        return "U"
    if direction == "D":
        if command == "R":
            return "L"
        return "R"
    if direction == "L":
        if command == "R":
            return "U"
        return "D"
    return command
while len(line) > 0:
    command = line[0]
    if command == "R" or command == "L":
        direction = new_direction(direction, command)
        line = line[1:]
    else:
        command = int(re.match("^[0-9]+", line).group(0))
        for _ in range(command):
            if direction == "U":
                current = current.up
            elif direction == "D":
                current = current.down
            elif direction == "L":
                current = current.left
            elif direction == "R":
                current = current.right
        line = line[len(str(command)):]
print(current.row+1, current.column+1, direction)
if direction == "R":
    facing = 0
if direction == "D":
    facing = 1
if direction == "L":
    facing = 2
if direction == "U":
    facing = 3
print((current.row+1)*1000 + (current.column+1)*4 + facing)