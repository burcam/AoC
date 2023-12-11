u_lines: list[list[str]] = []
with open("./11") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if any(l == '#' for l in line):
            u_lines.append(list(line))
        else:
            u_lines.append(list(line))
            u_lines.append(list(line))
start_len = len(u_lines[0])
exp_cols: list[int] = []
for x in range(start_len):
    if all(l[x] == '.' for l in u_lines):
        exp_cols.append(x)
for x in reversed(exp_cols):
    for line in u_lines:
        line.insert(x, ".")
gal_locs:list[tuple[int, int]] = []
for y in range(len(u_lines)):
    for x in range(len(u_lines[0])):
        if u_lines[y][x] == "#":
            gal_locs.append((y, x))
dist_sum = 0
for i in range(len(gal_locs)-1):
    for j in range(i+1, len(gal_locs)):
        dist_sum += abs(gal_locs[j][0] - gal_locs[i][0]) + abs(gal_locs[j][1] - gal_locs[i][1])
print(dist_sum)

u_lines: list[list[str]] = []
empty_y: list[int] = []
empty_x: list[int] = []
with open("./11") as file:
    y = 0
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if any(l == '#' for l in line):
            u_lines.append(list(line))
        else:
            u_lines.append(list(line))
            empty_y.append(y)
        y += 1
start_len = len(u_lines[0])
exp_cols: list[int] = []
for x in range(start_len):
    if all(l[x] == '.' for l in u_lines):
        empty_x.append(x)

gal_locs:list[tuple[int, int]] = []
y_offset = 0
for y in range(len(u_lines)):
    x_offset = 0
    if y in empty_y:
        y_offset += 999_999
        continue
    for x in range(len(u_lines[0])):
        if x in empty_x:
            x_offset += 999_999
        if u_lines[y][x] == "#":
            gal_locs.append((y+y_offset, x+x_offset))
dist_sum = 0
for i in range(len(gal_locs)-1):
    for j in range(i+1, len(gal_locs)):
        dist_sum += abs(gal_locs[j][0] - gal_locs[i][0]) + abs(gal_locs[j][1] - gal_locs[i][1])
print(dist_sum)

