import functools
import re
import time
from typing import Dict, List, Set, Tuple

minutes = 30
class Valve():
    name: str
    rate: int
    conn: List['Valve_Distance']
    direct_conn: List['Valve']
    conn_names = List[str]
    max_rates: Dict[int, List['Valve_Distance']]
    open: bool
    index: int
    def __init__(self, name, rate, conn_names) -> None:
        self.name = name
        self.rate = rate
        self.conn = []
        self.conn_names = conn_names
        self.max_rates = { 1: [Valve_Distance(self, 0)] }
        self.direct_conn = []
        self.open = False

class Valve_Distance():
    valve: Valve
    distance: int
    def __init__(self, valve, distance) -> None:
        self.valve = valve
        self.distance = distance
    def print(self):
        print(self.valve.name, self.distance)

class Person():
    location: Valve
    def travel_to(self, location: Valve):
        distance = next(conn.distance for conn in self.location.conn if conn.valve == location)
        self.location = location
        self.minutes -= distance
    def open_location(self):
        if self.location.open:
            return
        self.location.open = True
        self.minutes -= 1
        self.release += self.minutes* self.location.rate
    def __init__(self, minutes):
        self.minutes: int = minutes
        self.release: int = 0

v_dict: Dict[str, Valve] = {}
with open("day16") as file:
    for line in file.readlines():
        line = line.strip()
        matches = re.match("Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)$", line).groups()
        valve = Valve(matches[0], int(matches[1]), matches[2].split(", "))
        v_dict.setdefault(valve.name, valve)
valves: List[Valve] = []
for valve in v_dict.values():
    valve.conn = [Valve_Distance(v_dict[key], 1) for key in valve.conn_names ]
    valve.direct_conn = [v_dict[key] for key in valve.conn_names]
    valve.conn.insert(0, Valve_Distance(valve, 0))
    valves.append(valve)

for valve in v_dict.values():
    for i in range(2, minutes):
        new_children: List[Valve_Distance] = []
        names = [c.valve.name for c in valve.conn]
        names.append(valve.name)
        for conn in [conn for conn in valve.conn if conn.distance==i-1]:
            for child_valve in conn.valve.direct_conn:
                if child_valve.name not in names:
                    new_children.append(Valve_Distance(child_valve, i))
                    names.append(child_valve.name)
        for child in new_children:
            valve.conn.append(child)
        if not new_children:
            break
valves.sort(key=lambda valve: next(conn.distance for conn in valve.conn if conn.valve.name == "AA"))
for index, valve in enumerate(valves):
    valve.index = index
result = 0
depth = 10
for i in range(2, minutes):
    for valve in valves:
        next_rates: List[Valve_Distance] = []
        for connection in [conn for conn in valve.conn if conn.distance == i-1]:
            next_rates.append(connection)
        next_rates.extend(valve.max_rates[i-1])
        next_rates.sort(key=lambda conn: conn.valve.rate*(i - conn.distance), reverse=True)
        valve.max_rates.setdefault(i, next_rates)

open_valves = [valve.rate == 0 for valve in valves]

def get_valve_combos(valve: Valve, open: bool):
    combos: List[Tuple[int, bool]] = []
    if not open:
        for conn in valve.direct_conn:
            if conn.rate > 2 * valve.rate:
                break
        else:
            combos.append((valve.index, True))
    for conn in valve.direct_conn:
        combos.append((conn.index, False))
    return combos

@functools.cache
def simple_maximize(minutes: int, index: int, *open_valves: List[bool]):
    open_valves = list(open_valves)
    maximum = 0
    opened_valves = list(open_valves)
    if minutes < 1:
        return 0, opened_valves
    valve = valves[index]
    valve_combos = get_valve_combos(valve, open_valves[index])
    for index, open in valve_combos:
        open_bonus = 0
        if open:
            open_bonus += valve.rate*(minutes-1)
            open_valves[index] = True
            r = valve.rate
            valve.rate = 0
        temp, _ret = simple_maximize(minutes-1, index, *open_valves)
        temp += open_bonus
        if temp > maximum:
            maximum = temp
            opened_valves = list(_ret)
        if open:
            open_valves[index] = False
            valve.rate = r
    return maximum, opened_valves

@functools.cache
def maximize_pressure(minutes: int, index1: int, index2: int, *open_valves: List[bool]):
    open_valves = list(open_valves)
    maximum = 0
    if minutes < 1:
        return 0
    valve1 = valves[index1]
    valve2 = valves[index2]
    intersect = False
    nearconn1 = [conn.valve.name for conn in valve1.conn if conn.distance < minutes]
    nearconn2 = [conn.valve.name for conn in valve2.conn if conn.distance < minutes]
    for name in nearconn1:
        if name in nearconn2:
            intersect = True
            break
    if not intersect:
        return simple_maximize(minutes, index1, *open_valves)[0] + simple_maximize(minutes, index2, *open_valves)[0]
    valve1_combos = get_valve_combos(valve1, open_valves[index1])
    valve2_combos = get_valve_combos(valve2, open_valves[index2])
    if valve1_combos[0] == valve2_combos[0] and valve1_combos[0][1]:
        valve2_combos.pop(0)

    for index_1, open1 in valve1_combos:
        if open1:
            open_valves[index_1] = True
            r1 = valve1.rate
            valve1.rate = 0
        for index_2, open2 in valve2_combos:
            open_bonus = 0
            if open1:
                open_bonus += r1*(minutes-1)
            if open2:
                open_bonus += valve2.rate*(minutes-1)
                open_valves[index_2] = True
                r2 = valve2.rate
                valve2.rate = 0

            temp = maximize_pressure(minutes - 1, min(index_1, index_2), max(index_1, index_2), *open_valves)
            temp += open_bonus
            if temp > maximum:
                maximum = temp
            if open2:
                open_valves[index_2] = False
                valve2.rate = r2
        if open1:
            open_valves[index_1] = False
            valve1.rate = r1
    return maximum
start = time.perf_counter()
def get_time():
    return time.perf_counter() - start
pressure, open_valves1 = simple_maximize(5, 0, *open_valves)
pressure1, _ = simple_maximize(5, 0, *open_valves1)
print("05", pressure+pressure1, get_time())
pressure, open_valves1 = simple_maximize(15, 0, *open_valves)
pressure1, _ = simple_maximize(15, 0, *open_valves1)
print(15, pressure+pressure1, get_time())
pressure, open_valves1 = simple_maximize(26, 0, *open_valves)
pressure1, _ = simple_maximize(26, 0, *open_valves1)
print(26, pressure+pressure1, get_time())

print("05", maximize_pressure(5, 0, 0, *open_valves), get_time())
print(10, maximize_pressure(10, 0, 0, *open_valves), get_time())
print(15, maximize_pressure(15, 0, 0, *open_valves), get_time())
print(16, maximize_pressure(16, 0, 0, *open_valves), get_time())
print(17, maximize_pressure(17, 0, 0, *open_valves), get_time())
print(18, maximize_pressure(18, 0, 0, *open_valves), get_time())
print(19, maximize_pressure(19, 0, 0, *open_valves), get_time())
print(20, maximize_pressure(20, 0, 0, *open_valves), get_time())
print(21, maximize_pressure(21, 0, 0, *open_valves), get_time())
print(22, maximize_pressure(22, 0, 0, *open_valves), get_time())
print(23, maximize_pressure(23, 0, 0, *open_valves), get_time())
print(24, maximize_pressure(24, 0, 0, *open_valves), get_time())
print(25, maximize_pressure(25, 0, 0, *open_valves), get_time())
print(26, maximize_pressure(26, 0, 0, *open_valves), get_time())
# person = Person(minutes)
# person.location = valves[0]

# person.travel_to(v_dict["DD"])
# person.open_location()
# person.travel_to(v_dict["BB"])
# person.open_location()
# person.travel_to(v_dict["JJ"])
# person.open_location()
# person.travel_to(v_dict["HH"])
# person.open_location()
# person.travel_to(v_dict["EE"])
# person.open_location()
# person.travel_to(v_dict["CC"])
# person.open_location()
# #Release = 0*(30-x1) + 13*(30-x2) + 2*(30-x3) + 20*(30-x4)... = 30*SUM(flows) - SUM(flowi*xi)
# print(person.release)