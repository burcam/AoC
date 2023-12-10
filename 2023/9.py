with open("./9") as f:
    ext_sum = 0
    for l in f.readlines():
        numbers = [int(n) for n in l.strip().split(" ")]
        cont = True
        num_groups: list[list[int]] = [numbers]
        while cont:
            next_num = []
            cont = False
            cur_nums = num_groups[-1]
            for i in range(len(cur_nums)-1):
                n = cur_nums[i+1] - cur_nums[i]
                if n != 0:
                    cont = True
                next_num.append(n)
            num_groups.append(next_num)
        working = 0
        for g in reversed(num_groups):
            
            working = g[-1] + working
        ext_sum += working
print(ext_sum)

with open("./9") as f:
    ext_sum = 0
    for l in f.readlines():
        numbers = [int(n) for n in l.strip().split(" ")]
        cont = True
        num_groups: list[list[int]] = [numbers]
        while cont:
            next_num = []
            cont = False
            cur_nums = num_groups[-1]
            for i in range(len(cur_nums)-1):
                n = cur_nums[i+1] - cur_nums[i]
                if n != 0:
                    cont = True
                next_num.append(n)
            num_groups.append(next_num)
        working = 0
        for g in reversed(num_groups):
            working = g[0] - working
        ext_sum += working
print(ext_sum)