important_cycles = [20, 60, 100, 140, 180, 220]

with open("day10") as file:
    sum = 0
    x = 1
    lines = file.readlines()
    cycle = 0
    output = ""
    for line in lines:
        line = line.strip().split(" ")
        if line[0] == "noop":
            num = "0"
        else:
            num = line[1]
        cycle += 1
        print(cycle, x)
        if ((cycle-1)%40) - 1 <= (x%40) <= ((cycle-1)%40) + 1:
            output += "#"
        else:
            output += "."
        if (cycle%40) == 0:
            output += "\n"
        if line[0] != "noop":
            cycle += 1
            print(cycle, x)
            if ((cycle-1)%40) - 1 <= (x%40) <= ((cycle-1)%40) + 1:
                output += "#"
            else:
                output += "."
            if (cycle%40) == 0:
                output += "\n"
        x += int(num)
print(output)