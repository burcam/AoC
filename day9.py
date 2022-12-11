def update_tail(headpos, tailpos):
    res = [tailpos[0], tailpos[1]]
    if headpos[0] > tailpos[0] + 1:
        res[0] += 1
        if headpos[1] > tailpos[1]:
            res[1] += 1
        if headpos[1] < tailpos[1]:
            res[1] -= 1
        return (res[0], res[1])
    if headpos[0] < tailpos[0] - 1:
        res[0] -= 1
        if headpos[1] > tailpos[1]:
            res[1] += 1
        if headpos[1] < tailpos[1]:
            res[1] -= 1
        return (res[0], res[1])
    if headpos[1] > tailpos[1] + 1:
        res[1] += 1
        if headpos[0] > tailpos[0]:
            res[0] += 1
        if headpos[0] < tailpos[0]:
            res[0] -= 1
        return (res[0], res[1])
    if headpos[1] < tailpos[1] - 1:
        res[1] -= 1
        if headpos[0] > tailpos[0]:
            res[0] += 1
        if headpos[0] < tailpos[0]:
            res[0] -= 1
        return (res[0], res[1])

    return (res[0], res[1])
        

with open("day9") as file:
    visited = set()
    visited.add((0, 0))
    headpos = (0, 0)
    tailpos = [
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0),
                (0, 0)]
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        direction = line[0]
        movement = int(line[2:])
        if direction == "L":
            for i in range(movement):
                headpos = (headpos[0] - 1, headpos[1])
                tailpos[0] = update_tail(headpos, tailpos[0])
                for i in range(1, 9):
                    tailpos[i] = update_tail(tailpos[i-1], tailpos[i])
                visited.add((tailpos[8][0], tailpos[8][1]))
        elif direction == "R":
            for i in range(movement):
                headpos = (headpos[0] + 1, headpos[1])
                tailpos[0] = update_tail(headpos, tailpos[0])
                for i in range(1, 9):
                    tailpos[i] = update_tail(tailpos[i-1], tailpos[i])
                visited.add((tailpos[8][0], tailpos[8][1]))
        elif direction == "U":
            for i in range(movement):
                headpos = (headpos[0], headpos[1] + 1)
                tailpos[0] = update_tail(headpos, tailpos[0])
                for i in range(1, 9):
                    tailpos[i] = update_tail(tailpos[i-1], tailpos[i])
                visited.add((tailpos[8][0], tailpos[8][1]))
        elif direction == "D":
            for i in range(movement):
                headpos = (headpos[0], headpos[1] - 1)
                tailpos[0] = update_tail(headpos, tailpos[0])
                for i in range(1, 9):
                    tailpos[i] = update_tail(tailpos[i-1], tailpos[i])
                visited.add((tailpos[8][0], tailpos[8][1]))

print(len(visited))