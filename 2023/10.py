from dataclasses import dataclass
from enum import Enum

class PipeType(str, Enum):
    Vert = "|"
    Horiz = "-"
    NE = "L"
    NW = "J"
    SW = "7"
    SE = "F"
    GROUND = "."
    Start = "S"

class OutsideDir(int, Enum):
    N=1
    S=2
    E=3
    W=4

@dataclass(order=True, init=False)
class Point:
    def __init__(self, type, y, x, outside=None):
        self.type = type
        self.y=y
        self.x=x
        self.type=type
        self.outside=outside or []
    y: int
    x: int
    type: PipeType
    outside: list[OutsideDir]

def get_n(point: Point, pipes: list[str]):
    return Point(pipes[point.y-1][point.x], point.y-1, point.x)
def get_s(point: Point, pipes: list[str]):
    return Point(pipes[point.y+1][point.x], point.y+1, point.x)
def get_e(point: Point, pipes: list[str]):
    return Point(pipes[point.y][point.x+1], point.y, point.x+1)
def get_w(point: Point, pipes: list[str]):
    return Point(pipes[point.y][point.x-1], point.y, point.x-1)
pipe_arr: list[list[PipeType]] = []


with open("./10") as file:
    lines = file.readlines()
    row = 0

    for line in lines:
        line = line.strip()
        pipe_arr.append([PipeType(l) for l in line])
        col = 0
        for s in pipe_arr[-1]:
            if s == PipeType.Start:
                start = Point(PipeType.Start, row, col)
                break
            col += 1
        row += 1
def connection_points(p: Point, pipes: list[str]):
    match p.type:
        case PipeType.Vert:
            return get_n(p, pipes), get_s(p, pipes)
        case PipeType.Horiz:
            return get_w(p, pipes), get_e(p, pipes)
        case PipeType.NE:
            return get_n(p, pipes), get_e(p, pipes)
        case PipeType.NW:
            return get_n(p, pipes), get_w(p, pipes)
        case PipeType.SW:
            return get_s(p, pipes), get_w(p, pipes)
        case PipeType.SE:
            return get_s(p, pipes), get_e(p, pipes)

def start_type(p: Point, pipes: list[str]):
    directions = []
    if p.y-1 != -1:
        if pipes[p.y-1][p.x] in [PipeType.Vert, PipeType.SW, PipeType.SE]:
            directions.append("N")
    if p.y+1 != len(pipes):
        if pipes[p.y+1][p.x] in [PipeType.Vert, PipeType.NW, PipeType.NE]:
            directions.append("S")
    if p.x-1 != -1:
        if pipes[p.y][p.x-1] in [PipeType.Horiz, PipeType.SE, PipeType.NE]:
            directions.append("W")
    if p.y+1 != len(pipes[0]):
        if pipes[p.y][p.x+1] in [PipeType.Horiz, PipeType.SW, PipeType.NW]:
            directions.append("E")
    if "N" in directions:
        if "S" in directions:
            pipes[p.y][p.x] =  PipeType.Vert
            return PipeType.Vert
        if "E" in directions:
            pipes[p.y][p.x] =  PipeType.NE
            return PipeType.NE
        if "W" in directions:
            pipes[p.y][p.x] =  PipeType.NW
            return PipeType.NW
    if "S" in directions:
        if "E" in directions:
            pipes[p.y][p.x] =  PipeType.SE
            return PipeType.SE
        if "W" in directions:
            pipes[p.y][p.x] =  PipeType.SW
            return PipeType.SW
    pipes[p.y][p.x] =  PipeType.Horiz
    return PipeType.Horiz

start = Point(start_type(start, pipe_arr), start.y, start.x)
prevs = [start, start]
left, right = connection_points(start, pipe_arr)
steps = 1
while left != right:
    n_left = next(c for c in connection_points(left, pipe_arr) if c != prevs[0])
    n_right = next(c for c in connection_points(right, pipe_arr) if c != prevs[1])
    prevs = [left, right]
    left, right = n_left, n_right
    steps += 1
print(steps)

nodes = [start]
last_node = connection_points(start, pipe_arr)[1]
nodes.append(last_node)
lnode_idx = 0
while last_node != start:
    last_node = next(c for c in connection_points(last_node, pipe_arr) if c != nodes[lnode_idx])
    nodes.append(last_node)
    lnode_idx += 1
nodes.pop()
node_count = len(nodes)
sorted_nodes = sorted(nodes)
y_max = len(pipe_arr)-1
x_max = len(pipe_arr[0])-1



edge_node: Point = None
connections: list[OutsideDir] = []
for node in sorted_nodes:
    if node.x == 0:
        connections.append(OutsideDir.W)
        if node.type == PipeType.SE:
            connections.append(OutsideDir.N)
        if node.type == PipeType.NE:
            connections.append(OutsideDir.S)
        edge_node = node
        break
    if node.x == x_max:
        connections.append(OutsideDir.E)
        if node.type == PipeType.SW:
            connections.append(OutsideDir.N)
        if node.type == PipeType.NW:
            connections.append(OutsideDir.S)
        edge_node = node
        break
    if node.y == 0:
        connections.append(OutsideDir.N)
        if node.type == PipeType.SW:
            connections.append(OutsideDir.E)
        if node.type == PipeType.SE:
            connections.append(OutsideDir.W)
        edge_node = node
        break
    if node.y == y_max:
        connections.append(OutsideDir.S)
        if node.type == PipeType.NW:
            connections.append(OutsideDir.E)
        if node.type == PipeType.NE:
            connections.append(OutsideDir.W)
        edge_node = node
        break
def get_connections(point: Point, last_con_dir: OutsideDir):
    match point.type:
        case PipeType.NE:
            if last_con_dir == OutsideDir.N:
                return [OutsideDir.E]
            if last_con_dir == OutsideDir.E:
                return [OutsideDir.N]
            if last_con_dir == OutsideDir.W:
                return [OutsideDir.W, OutsideDir.S]
            return [OutsideDir.S, OutsideDir.W]
        case PipeType.NW:
            if last_con_dir == OutsideDir.N:
                return [OutsideDir.W]
            if last_con_dir == OutsideDir.W:
                return [OutsideDir.N]
            if last_con_dir == OutsideDir.E:
                return [OutsideDir.E, OutsideDir.S]
            return [OutsideDir.S, OutsideDir.E]
        case PipeType.SW:
            if last_con_dir == OutsideDir.S:
                return [OutsideDir.W]
            if last_con_dir == OutsideDir.W:
                return [OutsideDir.S]
            if last_con_dir == OutsideDir.E:
                return [OutsideDir.E, OutsideDir.N]
            return [OutsideDir.N, OutsideDir.E]
        case PipeType.SE:
            if last_con_dir == OutsideDir.S:
                return [OutsideDir.E]
            if last_con_dir == OutsideDir.E:
                return [OutsideDir.S]
            if last_con_dir == OutsideDir.W:
                return [OutsideDir.W, OutsideDir.N]
            return [OutsideDir.N, OutsideDir.W]
    return [last_con_dir]
connections = sorted(connections)
edge_node.outside = [*connections]
idx = nodes.index(edge_node) + 1
perimeter = len(connections)
counted = {(n.y, n.x) for n in nodes}
y_pos_min = sorted_nodes[0].y
y_pos_max = sorted_nodes[-1].y
x_pos_min = 1000
x_pos_max = 0
for i in range(node_count-1):
    node = nodes[(i+idx)%node_count]
    if node.x > x_pos_max:
        x_pos_max = node.x
    if node.x < x_pos_min:
        x_pos_min = node.x
    next_cons = get_connections(node, connections[-1])
    if not next_cons:
        ...
    elif len(next_cons) == 1:
        node.outside = next_cons
        connections.append(next_cons[0])
    elif next_cons[0] == connections[-1]:
        connections.append(next_cons[0])
        connections.append(next_cons[1])
        node.outside = next_cons
        continue
    else:
        connections.append(next_cons[1])
        connections.append(next_cons[0])
        node.outside = [next_cons[1], next_cons[0]]
outsides: set[tuple[int, int]] = set()
for node in nodes:
    for outside in node.outside:
        if outside == OutsideDir.N and (node.y-1, node.x) not in counted:
            outsides.add((node.y-1, node.x))
        if outside == OutsideDir.S and (node.y+1, node.x) not in counted:
            outsides.add((node.y+1, node.x))
        if outside == OutsideDir.W and (node.y, node.x-1) not in counted:
            outsides.add((node.y, node.x-1))
        if outside == OutsideDir.E and (node.y, node.x+1) not in counted:
            outsides.add((node.y, node.x+1))
last_enclosed = 1
enclosed = 0

while last_enclosed != enclosed:
    last_enclosed = enclosed
    enclosed = 0
    for y in range(y_pos_min, y_pos_max):
        for x in range(x_pos_min, x_pos_max):
            if (y, x) in counted:
                continue
            if (y, x) in outsides or (y+1, x) in outsides or (y-1, x) in outsides or (y, x+1) in outsides or (y, x-1) in outsides:
                outsides.add((y, x))
                continue
            enclosed += 1

print(enclosed)
# square: peri: num+4
# interior: (x_pos_max - x_pos_min - 1) * (y_pox_max - y_pos_min - 1)