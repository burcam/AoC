from dataclasses import dataclass
from functools import lru_cache

@dataclass
class Input:
    first: int
    range: int

@dataclass
class Map:
    input: int
    range: int
    offset: int

seed_soil_map = None
soil_fert_map = None
fert_water_map = None
water_light_map = None
light_temp_map = None
temp_hum_map = None
hum_loc_map = None
def read_mapping(lines: list[str], idx: int):
    soil_map: list[Map] = []
    line_len = len(lines)
    while idx < line_len and lines[idx].strip():
        tup = tuple(int(l) for l in lines[idx].strip().split(" "))
        m = Map(tup[1], tup[2], tup[0]-tup[1])
        soil_map.append(m)
        idx += 1
    soil_map = sorted(soil_map, key= lambda x: x.input)
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
    with open("./5") as f:
        lines = f.readlines()
        seeds_init = [int(seed) for seed in lines[0].split(":")[1].strip().split(" ")]
        seeds: list[Input] = []
        for i in range(0, len(seeds_init), 2):
            seeds.append(Input(seeds_init[i], seeds_init[i+1]))
        seeds = sorted(seeds, key= lambda x: x.first)
        idx = 3
        seed_soil_map, idx = read_mapping(lines, idx)
        soil_fert_map, idx = read_mapping(lines, idx)
        fert_water_map, idx = read_mapping(lines, idx)
        water_light_map, idx = read_mapping(lines, idx)
        light_temp_map, idx = read_mapping(lines, idx)
        temp_hum_map, idx = read_mapping(lines, idx)
        hum_loc_map, idx = read_mapping(lines, idx)
        soils = next_inputs(seeds, seed_soil_map)
        print("soil", soils)
        ferts = next_inputs(soils, soil_fert_map)
        print("fert", ferts)
        water = next_inputs(ferts, fert_water_map)
        print("water", water)
        light = next_inputs(water, water_light_map, True)
        print("light", light)
        temp = next_inputs(light, light_temp_map)
        print("temp", temp)
        hum = next_inputs(temp, temp_hum_map)
        print("hum", hum)
        loc = next_inputs(hum, hum_loc_map)
        
        print(loc[0])

def next_inputs(input: list[Input], maps: list[Map], verb=False):
    inidx = 0
    mapidx = 0
    i_len = len(input)
    m_len = len(maps)
    output: list[Input] = []
    while inidx < i_len and mapidx < m_len:
        if verb:
            print(inidx, i_len, mapidx)
            print(output)
        if input[inidx].first < maps[mapidx].input:
            if input[inidx].first + input[inidx].range < maps[mapidx].input:
                
                output.append(Input(input[inidx].first, input[inidx].range))
                if verb:
                    print("fully before", output)
                inidx += 1
                continue
            
            diff = maps[mapidx].input - input[inidx].first
            output.append(Input(input[inidx].first, diff))
            input.insert(inidx + 1, Input(maps[mapidx].input, input[inidx].range - diff))
            if verb:
                print("before-into", output)
            i_len += 1
            inidx += 1
            continue
        if maps[mapidx].input <= input[inidx].first < maps[mapidx].input + maps[mapidx].range:
            if input[inidx].first + input[inidx].range < maps[mapidx].input + maps[mapidx].range:
                
                output.append(Input(input[inidx].first+maps[mapidx].offset, input[inidx].range))
                if verb:
                    print(input[inidx], maps[mapidx])
                    print("all-in", output)
                inidx += 1
                continue
            
            diff = maps[mapidx].input + maps[mapidx].range - input[inidx].first
            output.append(Input(input[inidx].first+maps[mapidx].offset, diff))
            if verb:
                print("mostly in", output)
                print(input[inidx], maps[mapidx])
            input.insert(inidx + 1, Input(input[inidx].first + diff, input[inidx].range - diff))
            i_len += 1
            inidx += 1
            mapidx += 1
            continue
        if verb:
            print("all after")
        mapidx += 1
    if verb:
        print(inidx, i_len, mapidx)
        print(output)
    while inidx < i_len:
        output.append(input[inidx])
        inidx += 1
    return sorted(output, key=lambda x: x.first)

execute()
