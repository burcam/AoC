from typing import Dict, List, Set, Tuple


min_x = 500
max_x = 0
max_y = 0
with open("day14") as file:
    for line in file.readlines():
        line = line.strip()
        rock_lines = line.split(" -> ")
        for rock_line in rock_lines:
            loc = rock_line.split(",")
            x_coord = int(loc[0])
            y_coord = int(loc[1])
            if x_coord < min_x:
                min_x = x_coord
            if x_coord > max_x:
                max_x = x_coord
            if y_coord > max_y:
                max_y = y_coord
print(min_x, max_x, max_y)
rock_locs: Dict[int, Set[int]] = { y: set() for y in range(max_y+3)}
with open("day14") as file:
    for line in file.readlines():
        line = line.strip()
        rock_lines = line.split(" -> ")
        [last_x, last_y] = [int(val) for val in rock_lines[0].split(",")]
        for rock_line in rock_lines:
            loc = rock_line.split(",")
            [x, y] = [int(val) for val in rock_line.split(",")]
            x1 = min(last_x, x)
            x2 = max(last_x, x)
            for n in range(x1, x2+1):
                rock_locs.get(y).add(n)
            y1 = min(last_y, y)
            y2 = max(last_y, y)
            for n in range(y1, y2+1):
                rock_locs.get(n).add(x)
            last_y = y
            last_x = x

for d1 in range(max_y+1):
    line = ""
    for d2 in range(min_x, max_x+1):
        if d2 in rock_locs.get(d1):
            line += "#"
        else:
            line += "."
    print(line)
sand_path = [(500,0)]
fallen = 0
print("----------------------")
floor = max_y + 2
y_loc = 0
while(True):
    if 500 in rock_locs.get(0):
        break
    y_loc = sand_path[-1][1]+1
    if y_loc == floor:
        rock_locs.get(y_loc-1).add(sand_path.pop()[0])
        fallen += 1
        continue
    rock_line = rock_locs.get(y_loc)
    if rock_line is None:
        continue
    if len(rock_line) == 0:
        sand_path.append((sand_path[-1][0], y_loc))
    elif sand_path[-1][0] not in rock_line:
        sand_path.append((sand_path[-1][0], y_loc))
    elif sand_path[-1][0]-1 not in rock_line:
        sand_path.append((sand_path[-1][0]-1, y_loc))
    elif sand_path[-1][0]+1 not in rock_line:
        sand_path.append((sand_path[-1][0]+1, y_loc))
    else:
        rock_locs.get(y_loc-1).add(sand_path.pop()[0])
        fallen += 1
true_min_x = 500
true_max_x = 500
for rock in rock_locs.values():
    for rock_loc in rock:
        if rock_loc< true_min_x:
            true_min_x = rock_loc
        if rock_loc > true_max_x:
            true_max_x = rock_loc
for d1 in range(max_y+1):
    line = ""
    for d2 in range(true_min_x, true_max_x+1):
        if d2 in rock_locs.get(d1):
            line += "#"
        else:
            line += "."
    print(line)
print(fallen)