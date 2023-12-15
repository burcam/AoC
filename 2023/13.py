
import dataclasses
from math import ceil




def process_line(line: str, x_possibilities: list[int], line_len: int, verbose=False):
    rem_pos = []
    x2 = 0
    for x in x_possibilities:
        x2 = 0
        while x + x2 + 1 < line_len and x - x2 >= 0:
            if line[x+x2+1] != line[x-x2]:
                rem_pos.append(x)
                break
            x2 += 1
    if verbose:
        print(line, x_possibilities, [x for x in x_possibilities if x not in rem_pos], rem_pos)
    for r in rem_pos:
        x_possibilities.remove(r)
def process_project(lines: list[str], old_x: int=-1, old_y:int=-1, verbose=False):
    old_x -= 1
    old_y -= 1
    y_len = len(lines)
    x_len = len(lines[0])
    x_possibilities = [i for i in range(x_len-1)]
    try:
        x_possibilities.remove(old_x)
    except:
        ...
    if verbose:
        print("BBB")
        for line in lines:
            print(line)
    for line in lines:
        if not x_possibilities:
            break
        process_line(line, x_possibilities, x_len, verbose)
    if x_possibilities:
        return(0, x_possibilities[-1]+1)

    y_vals: list[str] = []
    for y in range(x_len):
        vert_slice = str.join("", [line[y] for line in lines])
        y_vals.append(vert_slice)
    y_possibilities = [i for i in range(0, y_len-1)]
    try:
        y_possibilities.remove(old_y)
    except:
        ...
    if verbose:
        print(y_possibilities, old_y)
        print("---")
        print(y_len, len(y_vals[0]))
        print("+++")
        for line in y_vals:
            print(line)
    for line in y_vals:
        if not y_possibilities:
            break
        process_line(line, y_possibilities, y_len, verbose)
    if verbose:
        print(y_possibilities)
    if not y_possibilities:
        return (0, 0)
    y_mirror = y_possibilities[-1]+1

    return (y_mirror, 0)

def execute():
    with open("./13") as f:
        lines: list[list[line]] = []
        l_idx = 0
        lines.append([])
        for line in f.readlines():
            line = line.strip()
            if not line:
                l_idx += 1
                lines.append([])
                continue
            lines[l_idx].append(line)
        tot = 0
        for line_group in lines:
            y, x = process_project(line_group)
            tot += x + y*100
        print(tot)
        
#execute()


def execute2():
    with open("./13") as f:
        lines: list[list[str]] = []
        l_idx = 0
        lines.append([])
        for line in f.readlines():
            line = line.strip()
            if not line:
                l_idx += 1
                lines.append([])
                continue
            lines[l_idx].append(line)
        tot = 0
        for line_group in lines:
            found = False
            old_y, old_x = process_project(line_group)
            for y in range(len(line_group)):
                if found:
                    break
                for x in range(len(line_group[0])):
                    char = '#'
                    if line_group[y][x] == "#":
                        char = '.'

                    line_group[y] = line_group[y][:x] + char + line_group[y][x+1:]

                    new_y, new_x = process_project(line_group, old_x, old_y)
                    char = '#' if char == '.' else '.'
                    line_group[y] = line_group[y][:x] + char + line_group[y][x+1:]
                    if new_y == old_y and new_x == old_x:
                        continue
                    if new_x or new_y:
                        tot += new_x + new_y*100
                        found = True
                        break
            if not found:
                print("not found")
                for line in line_group:
                    print(line)
                break
        print(tot)
execute2()
#26512 high
#15106 low
