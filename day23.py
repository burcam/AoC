from dataclasses import dataclass
from enum import Enum
import functools
from math import ceil
import re
import time
from typing import Dict, List, Set, Tuple

elves: Dict[Tuple[int, int], 'Elf'] = {}

@dataclass
class Elf():
    row: int
    column: int
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Elf) and self.row == __o.row and self.column == __o.column
    def __hash__(self) -> int:
        return (self.row, self.column).__hash__()
    def _check_N(self, elf_keys: List[Tuple[int, int]]):
        if (self.row-1, self.column-1) not in elf_keys and (self.row-1, self.column) not in elf_keys and (self.row-1, self.column+1) not in elf_keys:
            return (self.row-1, self.column)
        return False
    def _check_S(self, elf_keys: List[Tuple[int, int]]):
        if (self.row+1, self.column-1) not in elf_keys and (self.row+1, self.column) not in elf_keys and (self.row+1, self.column+1) not in elf_keys:
            return (self.row+1, self.column)
        return False
    def _check_W(self, elf_keys: List[Tuple[int, int]]):
        if (self.row-1, self.column-1) not in elf_keys and (self.row, self.column-1) not in elf_keys and (self.row+1, self.column-1) not in elf_keys:
            return (self.row, self.column-1)
        return False
    def _check_E(self, elf_keys: List[Tuple[int, int]]):
        if (self.row-1, self.column+1) not in elf_keys and (self.row, self.column+1) not in elf_keys and (self.row+1, self.column+1) not in elf_keys:
            return (self.row, self.column+1)
        return False
    

    def propose(self, round: int):
        elf_keys = elves.keys()
        if (
            (self.row-1, self.column-1) not in elf_keys and
            (self.row-1, self.column) not in elf_keys and
            (self.row-1, self.column+1) not in elf_keys and
            (self.row, self.column-1) not in elf_keys and
            (self.row, self.column+1) not in elf_keys and
            (self.row+1, self.column-1) not in elf_keys and
            (self.row+1, self.column) not in elf_keys and
            (self.row+1, self.column+1) not in elf_keys
        ):
            return False
        checks = [self._check_E, self._check_N, self._check_S, self._check_W]
        # print("  ", checks[round%4](elf_keys))
        # print("  ", checks[(round+1)%4](elf_keys))
        # print("  ", checks[(round+2)%4](elf_keys))
        # print("  ", checks[(round+3)%4](elf_keys))
        return checks[round%4](elf_keys) or checks[(round+1)%4](elf_keys) or checks[(round+2)%4](elf_keys) or checks[(round+3)%4](elf_keys)


def print_garden(elves: Dict[Tuple[int, int], Elf]):
    keys = list(elves.keys())
    keys.sort()
    top = keys[0][0]
    bottom = keys[-1][0]
    left = min(key[1] for key in keys)
    right = max(key[1] for key in keys)
    for row in range(top, bottom+1):
        line = ""
        for col in range(left, right+1):
            if (row, col) in keys:
                line += "#"
            else:
                line += "."
        print(line)





with open("day23") as file:
    lines = file.readlines()
for row, line in enumerate(lines):
    line = line.strip("\n")
    for col, char in enumerate(line):
        if char == "#":
            elves.setdefault((row, col), Elf(row, col))
print_garden(elves)
i = 1
movers = elves.keys()
while True:
    props: Dict[Tuple[int, int], List[Elf]] = {}
    for elf in movers:
        prop = elves[elf].propose(i)
        if not prop:
            continue
        if prop in props.keys():
            props[prop].append(elves[elf])
        else:
            props.setdefault(prop, [elves[elf]])
    moved: List[Elf] = []
    for move, elf in props.items():
        if len(elf) > 1:
            continue
        elf = elf[0]
        moved.append(elf)
        elves.pop((elf.row, elf.column))
        elf.row = move[0]
        elf.column = move[1]
        elves.setdefault((elf.row, elf.column), elf)
    if i%100 == 0:
        print(f"== Round {i} ==> {len(moved)}")
    #print_garden(elves)
    #print("")
    if len(moved) == 0:
        break
    i += 1
print(f"== Round {i} ==> {len(moved)}")
print_garden(elves)
#986 - low
#1021 - low
#1323 - high
keys = list(elves.keys())
keys.sort()
top = keys[0][0]
bottom = keys[-1][0]
left = min(key[1] for key in keys)
right = max(key[1] for key in keys)
print((bottom+1-top)*(right+1-left) - len(keys))