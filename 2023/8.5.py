import bisect
from collections import OrderedDict, deque
from dataclasses import dataclass
from functools import lru_cache
import math


class Line:
    def __init__(self, val: str, left: "Line" = None, right: "Line" = None) -> None:
        self.val = val
        self.l = left
        self.r = right
    val: str
    l: "Line" = None
    r: "Line" = None
    def __hash__(self) -> int:
        return hash(self.val)
    def __lt__(self, other):
        return self.val < other.val
    def __repr__(self) -> str:
        return f"[val: {self.val}, left: {self.l.val}, right: {self.r.val}]"

with open('./8') as f:
    ls = f.readlines()
inst = ls[0].strip()
inst_len = len(inst)
lines: list[Line] = []
line_dict: dict[str, Line] = {}
for line in ls[2:]:
    splits = line.strip().split(" ")
    a = splits[0][::-1]
    b = splits[2].strip("(,")[::-1]
    c = splits[3].strip(")")[::-1]
    def_a = line_dict.get(a, Line(a))
    if a != b:
        left = line_dict.get(b, Line(b))
    else:
        left = def_a
    if a != c:
        right = line_dict.get(c, Line(c))
    else:
        right = def_a
    def_a.l = left
    def_a.r = right
    line_dict.setdefault(a, def_a)
lines = sorted(line_dict.values())
for line in lines:
    line.r = line_dict[line.r.val]
    line.l = line_dict[line.l.val]


a_pref: list[Line] = []
for line in lines:
    if line.val[0] != 'A':
        break
    a_pref.append(line)
i = 0
cont = True

def next_z(pref: Line, inst: str, inst_idx: int):
    inst_len = len(inst)
    if inst[inst_idx] == 'L':
        next_pref = pref.l
    else:
        next_pref = pref.r
    inst_idx += 1
    count = 1
    while next_pref.val[0] != 'Z':
        if inst[inst_idx%inst_len] == 'L':
            next_pref = next_pref.l
        else:
            next_pref = next_pref.r
        inst_idx += 1
        count += 1
    return count, next_pref
print(a_pref)
@dataclass(order=True)
class Z:
    steps: int
    inst_idx: int
    working: Line


def get_next(working: Line, inst: str, inst_idx: int):
    if inst[inst_idx] == 'L':
        working = working.l
    else:
        working = working.r
    inst_idx = (inst_idx+1)%inst_len
    return inst_idx, working
@lru_cache()
def get_next_z(working: Line, inst: str, inst_idx: int):
    inst_idx, working = get_next(working, inst, inst_idx)
    steps = 1
    while working.val[0] != 'Z':
        inst_idx, working = get_next(working, inst, inst_idx)
        steps += 1
    return (steps, inst_idx, working)

stepwork: deque[Z] = []

for pref in a_pref:
    k = get_next_z(pref, inst, 0)
    print(k, Z(*k))
    stepwork.append(Z(*k))
stepwork = deque(sorted(stepwork))
print(math.lcm(*[s.steps for s in stepwork]))
slen = len(stepwork)
cycles = 0
while stepwork[0].steps != stepwork[-1].steps:
    cycles += 1
    
    min_step = stepwork.pop()
    if cycles % 1000 == 0:
        print(min_step)
    next_step = Z(*get_next_z(min_step.working, inst, min_step.inst_idx))
    next_step.steps += min_step.steps
    break
    for i in range(slen-1):
        if stepwork[i] < next_step:
            stepwork.insert(i, next_step)
            break
    if len(stepwork) < slen:
        stepwork.append(next_step)
print(cycles)
print(stepwork)
# 850669 low