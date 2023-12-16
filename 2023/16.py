from dataclasses import dataclass
from enum import Enum
import sys

sys.setrecursionlimit(1_000_000_000)

class TileType(str, Enum):
    Empty="."
    LMirror="/"
    RMirror="\\"
    VertSplit="|"
    HorizSplit="-"


@dataclass(frozen=True)
class Point:
    y: int
    x: int

class Direction(str, Enum):
    U="U"
    D="D"
    R="R"
    L="L"

@dataclass
class Tile:
    loc: Point
    type: TileType
    seen: list[Direction]

def move_empty(cur_pos: Tile, dir: Direction, y_height: int, x_len: int):
    if cur_pos.loc.y == 0 and dir == Direction.U:
        return []
    if cur_pos.loc.x == 0 and dir == Direction.L:
        return []
    if cur_pos.loc.y == y_height-1 and dir == Direction.D:
        return []
    if cur_pos.loc.x == x_len-1 and dir == Direction.R:
        return []

    match dir:
        case Direction.U:
            return [(Point(cur_pos.loc.y-1, cur_pos.loc.x), dir)]
        case Direction.D:
            return [(Point(cur_pos.loc.y+1, cur_pos.loc.x), dir)]
        case Direction.L:
            return [(Point(cur_pos.loc.y, cur_pos.loc.x-1), dir)]
        case Direction.R:
            return [(Point(cur_pos.loc.y, cur_pos.loc.x+1), dir)]
    return[]

def move_lmirror(cur_pos: Tile, dir: Direction, y_height: int, x_len: int):
    if cur_pos.loc.y == 0 and dir == Direction.R:
        return []
    if cur_pos.loc.x == 0 and dir == Direction.D:
        return []
    if cur_pos.loc.y == y_height-1 and dir == Direction.L:
        return []
    if cur_pos.loc.x == x_len-1 and dir == Direction.U:
        return []
    match dir:
        case Direction.U:
            return [(Point(cur_pos.loc.y, cur_pos.loc.x+1), Direction.R)]
        case Direction.D:
            return [(Point(cur_pos.loc.y, cur_pos.loc.x-1), Direction.L)]
        case Direction.L:
            return [(Point(cur_pos.loc.y+1, cur_pos.loc.x), Direction.D)]
        case Direction.R:
            return [(Point(cur_pos.loc.y-1, cur_pos.loc.x), Direction.U)]
    return []

def move_rmirror(cur_pos: Tile, dir: Direction, y_height: int, x_len: int):
    if cur_pos.loc.y == 0 and dir == Direction.L:
        return []
    if cur_pos.loc.x == 0 and dir == Direction.U:
        return []
    if cur_pos.loc.y == y_height-1 and dir == Direction.R:
        return []
    if cur_pos.loc.x == x_len-1 and dir == Direction.D:
        return []
    match dir:
        case Direction.D:
            return [(Point(cur_pos.loc.y, cur_pos.loc.x+1), Direction.R)]
        case Direction.U:
            return [(Point(cur_pos.loc.y, cur_pos.loc.x-1), Direction.L)]
        case Direction.R:
            return [(Point(cur_pos.loc.y+1, cur_pos.loc.x), Direction.D)]
        case Direction.L:
            return [(Point(cur_pos.loc.y-1, cur_pos.loc.x), Direction.U)]
    return []
def vert_split(cur_pos: Tile, dir: Direction, y_height: int):
    if dir == Direction.U:
        if cur_pos.loc.y == 0:
            return []
        return [(Point(cur_pos.loc.y-1, cur_pos.loc.x), Direction.U)]
    if dir == Direction.D:
        if cur_pos.loc.y == y_height-1:
            return []
        return [(Point(cur_pos.loc.y+1, cur_pos.loc.x), Direction.D)]
    if cur_pos.loc.y == 0:
        return [(Point(cur_pos.loc.y+1, cur_pos.loc.x), Direction.D)]
    if cur_pos.loc.y == y_height-1:
        return [(Point(cur_pos.loc.y-1, cur_pos.loc.x), Direction.U)]
    return [(Point(cur_pos.loc.y+1, cur_pos.loc.x), Direction.D), (Point(cur_pos.loc.y-1, cur_pos.loc.x), Direction.U)]

def horiz_split(cur_pos: Tile, dir: Direction, x_len: int):
    if dir == Direction.L:
        if cur_pos.loc.x == 0:
            return []
        return [(Point(cur_pos.loc.y, cur_pos.loc.x-1),Direction.L)]
    if dir == Direction.R:
        if cur_pos.loc.x == x_len-1:
            return []
        return [(Point(cur_pos.loc.y, cur_pos.loc.x+1),Direction.R)]
    if cur_pos.loc.x == 0:
        return [(Point(cur_pos.loc.y, cur_pos.loc.x+1),Direction.R)]
    if cur_pos.loc.x == x_len-1:
        return [(Point(cur_pos.loc.y, cur_pos.loc.x-1),Direction.L)]
    return [(Point(cur_pos.loc.y, cur_pos.loc.x+1),Direction.R), (Point(cur_pos.loc.y, cur_pos.loc.x-1),Direction.L)]

unique_seen = 0
def light_movement(cur_pos: Tile, dir: Direction, tiles: dict[Point, Tile], y_height: int, x_len: int):
    global unique_seen
    if dir in cur_pos.seen:
        return
    if not cur_pos.seen:
        unique_seen += 1
    cur_pos.seen.append(dir)
    match cur_pos.type:
        case TileType.Empty:
            next_points = move_empty(cur_pos, dir, y_height, x_len)
        case TileType.LMirror:
            next_points = move_lmirror(cur_pos, dir, y_height, x_len)
        case TileType.RMirror:
            next_points = move_rmirror(cur_pos, dir, y_height, x_len)
        case TileType.VertSplit:
            next_points = vert_split(cur_pos, dir, y_height)
        case TileType.HorizSplit:
            next_points = horiz_split(cur_pos, dir, x_len)
    for next_point in next_points:
        light_movement(tiles[next_point[0]], next_point[1], tiles, y_height, x_len)

def execute():
    with open("./16") as file:
        lines = [l.strip() for l in file.readlines()]
    tiles = {}
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            tiles[Point(y, x)] = Tile(Point(y, x), lines[y][x], [])
    light_movement(tiles[Point(0, 0)], Direction.R, tiles, len(lines), len(lines[0]))
execute()
print(unique_seen)

def reset_tiles(tiles: list[Tile]):
    for tile in tiles:
        tile.seen = []

def execute2():
    global unique_seen
    unique_seen = 0
    with open("./16") as file:
        lines = [l.strip() for l in file.readlines()]
    tiles = {}
    tile_list = []
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            tile = Tile(Point(y, x), lines[y][x], [])
            tile_list.append(tile)
            tiles[Point(y, x)] = tile
    cur_max = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if y == 0:
                light_movement(tiles[Point(y, x)], Direction.D, tiles, len(lines), len(lines[0]))
                reset_tiles(tile_list)
                cur_max = max(cur_max, unique_seen)
                unique_seen = 0
            if y == len(lines) - 1:
                light_movement(tiles[Point(y, x)], Direction.U, tiles, len(lines), len(lines[0]))
                reset_tiles(tile_list)
                cur_max = max(cur_max, unique_seen)
                unique_seen = 0
            if x == 0:
                light_movement(tiles[Point(y, x)], Direction.R, tiles, len(lines), len(lines[0]))
                reset_tiles(tile_list)
                cur_max = max(cur_max, unique_seen)
                unique_seen = 0
            if x == len(lines[0]) - 1:
                light_movement(tiles[Point(y, x)], Direction.L, tiles, len(lines), len(lines[0]))
                reset_tiles(tile_list)
                cur_max = max(cur_max, unique_seen)
                unique_seen = 0
    print(cur_max)
execute2()
# high 14148
# low 7086