import bisect
from dataclasses import dataclass

def find_idx(cur: str, dir: list[str]):
    return bisect.bisect_left(dir, (cur))


with open('./8') as f:
    lines = f.readlines()
    inst = lines[0].strip()
sort_dir = sorted(lines[2:])
current = 'AAA'
steps = 0
inst_len = len(inst)
c_idx = 0
while current != 'ZZZ':
    steps += 1
    L, R = sort_dir[c_idx][7:-1].split(",")
    L = L.strip().strip("()")
    R = R.strip().strip("()")
    if inst[(steps-1) % inst_len] == 'L':
        current = L
        c_idx = find_idx(L, sort_dir)
    else:
        current = R
        c_idx = find_idx(R, sort_dir)
print(steps)

@dataclass
class Line:
    val: str
    l: str
    r: str
    def __lt__(self, other):
        return self.val < other.val

with open('./8') as f:
    ls = f.readlines()
inst = ls[0].strip()
inst_len = len(inst)
lines: list[Line] = []
for line in ls[2:]:
    splits = line.strip().split(" ")
    a = splits[0]
    b = splits[2].strip("(,")
    c = splits[3].strip(")")
    l = Line(a[::-1], b[::-1], c[::-1])
    bisect.insort_left(lines, l)
sort_dir = lines
print(inst_len*len(sort_dir))
@dataclass
class ZVal:
    idx: int
    steps: int
    inst_idx: int
    def __lt__(self, other):
        return self.steps < other.steps
def find_line_idx(cur: str, dir: list[Line]):
    return bisect.bisect_left(dir, Line(cur, "", ""))


def get_next(inst: str, inst_idx: int, cur: Line, lines: list[Line]):
    if inst[inst_idx] == 'L':
        return find_line_idx(cur.l, lines)
    else:
        return find_line_idx(cur.r, lines)

fake_line = Line("", "", "")

def get_next_z(inst: str, inst_idx: int, inst_len: int, cur: Line) -> ZVal:
    global sort_dir
    if inst[inst_idx] == 'L':
        fake_line.val = cur.l
        next_idx = bisect.bisect_left(sort_dir, fake_line)
    else:
        fake_line.val = cur.r
        next_idx = bisect.bisect_left(sort_dir, fake_line)
    next_line = sort_dir[next_idx]
    if next_line.val[0] == 'Z':
        return ZVal(next_idx, 1, inst_idx)
    iterate = get_next_z(inst, (inst_idx+1) % inst_len, inst_len, next_line)
    return ZVal(iterate.idx, iterate.steps+1, iterate.inst_idx)


currents = sort_dir[:find_line_idx("B", sort_dir)]
inst_idx = 0
zeepers: list[ZVal] = []
for c in currents:
    zee = get_next_z(inst, 0, inst_len, c)
    bisect.insort_left(zeepers, zee)
print(zeepers)
while zeepers[0].steps != zeepers[-1].steps:
    fzee = zeepers.pop(0)
    zee = get_next_z(inst, zee.inst_idx, inst_len, sort_dir[zee.idx])
    zee.steps += fzee.steps - 1
    bisect.insort_left(zeepers, zee)
print(zeepers[0].steps)