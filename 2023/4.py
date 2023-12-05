with open("./4") as file:
    total = 0
    for line in file.readlines():
        line = line.strip()
        winning, real = line.split(":")[1].split("|")
        win_nums = sorted([int(num) for num in winning.split(" ") if num])
        real_nums = sorted([int(num) for num in real.split(" ") if num])
        points = 0.5
        real_idx = 0
        win_idx = 0
        real_len = len(real_nums)
        win_len = len(win_nums)
        while(real_idx < real_len and win_idx < win_len):
            real = real_nums[real_idx]
            win = win_nums[win_idx]
            if real == win:
                points *= 2
                real_idx += 1
            elif win > real:
                real_idx += 1
            else:
                win_idx += 1
        if points > 0.5:
            total += points
print(total)

with open("./4") as file:
    lines = file.readlines()
    line_counts = [1 for _ in range(len(lines))]
    line_idx = 0
    for line in lines:
        line = line.strip()
        winning, real = line.split(":")[1].split("|")
        win_nums = sorted([int(num) for num in winning.split(" ") if num])
        real_nums = sorted([int(num) for num in real.split(" ") if num])
        points = 0.5
        real_idx = 0
        win_idx = 0
        real_len = len(real_nums)
        win_len = len(win_nums)
        matches = 0
        while(real_idx < real_len and win_idx < win_len):
            real = real_nums[real_idx]
            win = win_nums[win_idx]
            if real == win:
                matches += 1
                real_idx += 1
            elif win > real:
                real_idx += 1
            else:
                win_idx += 1
        for inc in range(line_idx+1, line_idx+matches+1):
            line_counts[inc] += line_counts[line_idx]
        line_idx += 1
print(line_counts)
total = sum(line_counts)
print(total)
