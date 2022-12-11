with open("day8") as file:
    lines = file.readlines()
    tree_ids = []
    all_visible = set()
    for index, line in enumerate(lines):
        line = line.strip()
        visible = set()
        for i in range(len(line)):
            if i == 0:
                max = line[0]
                visible.add(i)
                continue
            if line[i] <= max:
                continue
            max = line[i]
            visible.add(i)
        for i in reversed(range(len(line))):
            if i == len(line) - 1:
                max = line[i]
                visible.add(i)
                continue
            if line[i] <= max:
                continue
            max = line[i]
            visible.add(i)
        for item in visible:
            all_visible.add(item+index*len(line))
    
    cols = []
    for index, line in enumerate(lines[0].strip()):
        cols.append("")
    for line in lines:
        index = 0
        for char in line.strip():
            cols[index] += char
            index += 1
    for index, line in enumerate(cols):
        line = line.strip()
        visible = set()
        for i in range(len(line)):
            if i == 0:
                max = line[0]
                visible.add(i)
                continue
            if line[i] <= max:
                continue
            max = line[i]
            visible.add(i)
        for i in reversed(range(len(line))):
            if i == len(line) - 1:
                max = line[i]
                visible.add(i)
                continue
            if line[i] <= max:
                continue
            max = line[i]
            visible.add(i)
        for item in visible:
            all_visible.add(index+item*len(cols))
print(len(all_visible))

max = 0
for index, line in enumerate(lines):
    line = line.strip()
    for r_index, c in enumerate(line):
        top = 0
        left = 0
        right = 0
        bottom = 0
        max_ = -1
        print(index, r_index)
        for i in reversed(range(index)):
            if int(lines[i][r_index]) < int(c):
                top += 1
            else:
                top += 1
                break
        
        max_ = -1
        for i in reversed(range(r_index)):
            if int(lines[index][i]) < int(c):
                left += 1
            else:
                left += 1
                break
        max_ = -1
        for i in range(r_index+1, len(line)):
            if int(lines[index][i]) < int(c):
                right += 1
            else:
                right += 1
                break
        max_ = -1
        for i in range(index+1, len(lines)):
            if int(lines[i][r_index]) < int(c):
                bottom += 1
            else:
                bottom += 1
                break
        prod = top*left*right*bottom
        print(top, left, right, bottom, prod)
        if prod > max:
            max = prod
print(max)