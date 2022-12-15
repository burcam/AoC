import re
from typing import Dict, List, Set, Tuple

excluded: List[List[Tuple[int,int]]] = [[] for _ in range(4000001)]

with open("day15") as file:
    for line in file.readlines():
        line = line.strip()
        print(line)
        matches = re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line).groups()
        [x,y,bx,by]=[int(match) for match in matches]
        distance = abs(x-bx) + abs(y-by)
        for y_val in range(max(0, y-distance), min(4000000, y+distance)+1):
            y_diff = abs(y-y_val)
            if y_val == 288625:
                print((max(0, x+y_diff-distance), min(4000000, x+distance-y_diff)))
            excluded[y_val].append((max(0, x+y_diff-distance), min(4000000, x+distance-y_diff)))

found = False
for index, exc in enumerate(excluded):
    exc.sort()
    line = [exc[0][0], exc[0][1]]
    for exc_index, ran in enumerate(exc):
        if exc_index == 0:
            continue
        if ran[0] > line[1] + 1:
            print(line[1], ran[0])
            print((line[1]+1)*4000000 + index)
            found = True
            break
        line[1] = max(line[1], ran[1])
    if found:
        break