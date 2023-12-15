from enum import Enum
from functools import lru_cache
import numpy as np

class Rock(str, Enum):
    Round="O"
    Cube="#"
    Ground="."

with open("./14") as f:
    lines = f.readlines()
    l2: list[str] = []
    for line in lines:
        l2.append(line.strip())
    lines = l2
    height = len(lines)
    axis_shift: list[list[Rock]] = []
    for i in range(len(lines[0])):
        axis_shift.append("".join([line[i] for line in lines]))

line_len = len(axis_shift[0])
total = 0
for line in axis_shift:
    idx = 0
    last_rock = -1
    line_tot = 0
    while idx < line_len:
        if line[idx] == Rock.Ground:
            idx += 1
            continue
        if line[idx] == Rock.Cube:
            last_rock = idx
            idx += 1
            continue
        line_tot += height - last_rock - 1
        last_rock = last_rock + 1
        idx += 1
    total += line_tot
print(total)

def mirror(items: tuple[tuple[Rock], ...]):
    new_items: list[list[Rock]] = []
    for i in range(len(items[0])):
        new_items.append("".join([item[i] for item in items]))
    return new_items

def remap_face(items: tuple[tuple[Rock], ...]):
    new_face: list[list[Rock]] = []
    for line in items:
        new_face.append([])
        idx = 0
        last_rock = -1
        while idx < line_len:
            if line[idx] == Rock.Ground:
                new_face[-1].append(Rock.Ground)
                idx += 1
                continue
            if line[idx] == Rock.Cube:
                new_face[-1].append(Rock.Cube)
                last_rock = idx
                idx += 1
                continue
            if last_rock + 1 == idx:
                new_face[-1].append(Rock.Round)
                last_rock += 1
            else:
                new_face[-1][last_rock+1] = Rock.Round
                last_rock += 1
                new_face[-1].append(Rock.Ground)
            idx += 1
    return new_face
def rotate_clock(items: tuple[tuple[Rock], ...]):
    final_arr: list[list[Rock]] = []
    y_len = len(items)

    for y in range(y_len):
        final_arr.append("".join([item[y] for item in items][::-1]))

    ts = []
    for line in final_arr:
        ts.append("".join(line))
    return tuple(ts)


@lru_cache
def run_cycle(items: tuple[tuple[Rock], ...]):
    north_face = mirror(remap_face(mirror(items)))
    west_face = mirror(remap_face(mirror(rotate_clock(north_face))))
    south_face = mirror(remap_face(mirror(rotate_clock(west_face))))
    east_face = mirror(remap_face(mirror(rotate_clock(south_face))))
    return rotate_clock(east_face)

cycle = tuple(lines)
for _ in range(1_000_000_000):
    cycle = run_cycle(cycle)
axis_shift: list[list[Rock]] = []


line_points = len(cycle)
total = 0
for i in range(len(cycle)):
    found = 0
    for l in cycle[i]:
        if l == Rock.Round:
            found += 1
    total += found*line_points
    line_points -= 1

print(total)