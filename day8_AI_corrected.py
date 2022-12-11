count = 0
input = open("day8")
grid = []
for line in input:
    grid.append(list(map(int, line.strip())))
count = 0
for i in range(len(grid)):
    for j in range(len(grid[i])):
        is_visible1, is_visible2, is_visible3, is_visible4 = True, True, True, True
        for k in range(j):
            if grid[i][j] <= grid[i][k]:
                is_visible1 = False
                break
        for k in range(j+1, len(grid[i])):
            if grid[i][j] <= grid[i][k]:
                is_visible2 = False
                break
        for k in range(i):
            if grid[i][j] <= grid[k][j]:
                is_visible3 = False
                break
        for k in range(i+1, len(grid)):
            if grid[i][j] <= grid[k][j]:
                is_visible4 = False
                break
        if is_visible1 or is_visible2 or is_visible3 or is_visible4:
            count += 1

print(count)