from functools import lru_cache

seed_soil_map = None
soil_fert_map = None
fert_water_map = None
water_light_map = None
light_temp_map = None
temp_hum_map = None
hum_loc_map = None
def read_mapping(lines: list[str], idx: int):
    soil_map: list[tuple[int, int, int]] = []
    line_len = len(lines)
    while idx < line_len and lines[idx].strip():
        tup = tuple(int(l) for l in lines[idx].strip().split(" "))
        soil_map.append((tup[1], tup[0], tup[2]))
        idx += 1
    soil_map = sorted(soil_map)
    idx += 2
    return soil_map, idx
def execute():
    global seed_soil_map
    global soil_fert_map
    global fert_water_map
    global water_light_map
    global light_temp_map
    global temp_hum_map
    global hum_loc_map
    with open("./5t") as f:
        lines = f.readlines()
        seeds_init = [int(seed) for seed in lines[0].split(":")[1].strip().split(" ")]
        seeds = []
        for i in range(0, len(seeds_init), 2):
            seeds.append((seeds_init[i], seeds_init[i+1]))
        seeds = sorted(seeds)
        idx = 3
        seed_soil_map, idx = read_mapping(lines, idx)
        soil_fert_map, idx = read_mapping(lines, idx)
        fert_water_map, idx = read_mapping(lines, idx)
        water_light_map, idx = read_mapping(lines, idx)
        light_temp_map, idx = read_mapping(lines, idx)
        temp_hum_map, idx = read_mapping(lines, idx)
        hum_loc_map, idx = read_mapping(lines, idx)
        best_seed_val = -1
        best_seed = 1_000_000_000_000
        for seed in seeds:
            seed_best = get_best_seed(seed)
            if seed_best < best_seed:
                best_seed = seed_best
                best_seed_val = seed
    print(best_seed)
    print(best_seed_val)

def get_best(input: list[tuple[int,int]], tups: list[tuple[int,int,int]]):
    inidx = 0
    tupidx = 0
    output: list[tuple[int,int]] = []
    inlen = len(input)
    tuplen = len(tups)
    while inidx < inlen and tupidx < tuplen:
        if input[inidx][0] + input[inidx][1] < tups[tupidx][0]:
            output.append(input[inidx])
            inidx += 1
            continue
        if input[inidx][0] < tuplen[tupidx][0]:
            output.append((input[inidx][0], tuplen[tupidx][0]-input[inidx][0]))
            input.insert(inidx+1, (input[inidx][0] + input[inidx][1] - tuplen[tupidx][0]))
            inlen += 1
            continue
        if input[inidx][0] + input[inidx][1] < tups[tupidx][1]:
            output.append((tups[inidx][0], input[inidx][1]))
            inidx += 1
            continue
        if input[inidx][0] < tups[tupidx][1]:
            output.append((tups[inidx][0], tups[tupidx][1] - input[inidx][0]))
            input.insert(inidx+1, (input[inidx][0] + input[inidx][1] - tuplen[tupidx][0]))
            inidx += 1
            continue
            
    for i in range(len(tups)):
        if tups[i][0] <= input < tups[i][0] + tups[i][2]:
            return tups[i][1] + (input - tups[i][0])
        elif i < len(tups)-1 and tups[i][0] < input < tups[i+1][0]:
            return input
    return input


def get_best_seed(seed: int):
    v = get_best(seed, seed_soil_map)
    return get_best_soil(v)

def get_best_soil(soil: int) -> int:
    v = get_best(soil, soil_fert_map)
    return get_best_fert(v)

def get_best_fert(fert: int):
    v = get_best(fert, fert_water_map)
    return get_best_water(v)

def get_best_water(water):
    v = get_best(water, water_light_map)
    return get_best_light(v)

def get_best_light(light):
    v = get_best(light, light_temp_map)
    return get_best_temp(v)

def get_best_temp(temp):
    v = get_best(temp, temp_hum_map)
    return get_best_hum(v)

def get_best_hum(hum):
    v = get_best(hum, hum_loc_map)
    return v

execute()