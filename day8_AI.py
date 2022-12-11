count = 0
input = open("day8")
grid = []
for line in input:
    grid.append(list(map(int, line.split())))
count = 0
for i in range(len(grid)):
    for j in range(len(grid[i])):
        is_visible = True
        for k in range(j):
            if grid[i][j] <= grid[i][k]:
                is_visible = False
                break
        for k in range(j+1, len(grid[i])):
            if grid[i][j] <= grid[i][k]:
                is_visible = False
                break
        for k in range(i):
            if grid[i][j] <= grid[k][j]:
                is_visible = False
                break
        for k in range(i+1, len(grid)):
            if grid[i][j] <= grid[k][j]:
                is_visible = False
                break
        if is_visible:
            count += 1

print(count)