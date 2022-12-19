from dataclasses import dataclass
import functools
from math import floor
from statistics import mean
from typing import Dict, List, Sequence, Set, TypeVar


with open("day17") as file:
    input = file.readline().strip()
jet_count = len(input)
T = TypeVar("T")
def infinite_iterator(iterable: Sequence[T]):
    while(True):
        for item in iterable:
            yield item
@dataclass(frozen=True)
class Point():
    x: int
    y: int
@dataclass(frozen=True)
class Shape():

    points: Set[Point]
    def left_points(self): Set[Point]
    def right_points(self): Set[Point]
    def down_points(self): Set[Point]
    def top(self): int
    root: Point


class Line(Shape):
    _left_point: Point
    _right_point: Point
    
    def left_points(self):
        return frozenset([self._left_point])
    def right_points(self):
        return frozenset([self._right_point])
    def down_points(self):
        return self.points
    def top(self):
        return 0
    def __init__(self, points: List[Point]):
        super().__init__(frozenset(points), Point(0,0))
        self._left_point = points[0]
        self._right_point = points[3]
    def __hash__(self):
        return super().__hash__()
class Cross(Shape):
    _left_points: Set[Point]
    _right_points: Set[Point]
    _down_points: Set[Point]
    
    def left_points(self):
        return self._left_points
    def right_points(self):
        return self._right_points
    def down_points(self):
        return self._down_points
    def top(self):
        return 2
    def __init__(self, points: List[Point]):
        super().__init__(frozenset(points), Point(0,0))
        self._left_points = frozenset([points[0], points[1], points[4]])
        self._right_points = frozenset([points[0], points[3], points[4]])
        self._down_points = frozenset([points[1], points[3], points[4]])
    def __hash__(self):
        return super().__hash__()

class JShape(Shape):
    _left_points: Set[Point]
    _right_points: Set[Point]
    _down_points: Set[Point]
    
    def left_points(self):
        return self._left_points
    def right_points(self):
        return self._right_points
    def down_points(self):
        return self._down_points
    def top(self):
        return 2
    def __init__(self, points: List[Point]):
        super().__init__(frozenset(points), Point(0,0))
        self._left_points = frozenset([points[0], points[1], points[2]])
        self._right_points = frozenset([points[0], points[1], points[4]])
        self._down_points = frozenset([points[2], points[3], points[4]])
    def __hash__(self):
        return super().__hash__()

class LShape(Shape):
    _down_points: Set[Point]
    
    def left_points(self):
        return self.points
    def right_points(self):
        return self.points
    def down_points(self):
        return self._down_points
    def top(self):
        return 3
    def __init__(self, points: List[Point]):
        super().__init__(frozenset(points), Point(0,0))
        self._down_points = frozenset([points[0]])
    def __hash__(self):
        return super().__hash__()

class Square(Shape):
    _left_points: Set[Point]
    _right_points: Set[Point]
    _down_points: Set[Point]
    
    def left_points(self):
        return self._left_points
    def right_points(self):
        return self._right_points
    def down_points(self):
        return self._down_points
    def top(self):
        return 1
    def __init__(self, points: List[Point]):
        super().__init__(frozenset(points), Point(0,0))
        self._left_points = frozenset([points[0], points[2]])
        self._right_points = frozenset([points[1], points[3]])
        self._down_points = frozenset([points[0], points[1]])
    def __hash__(self):
        return super().__hash__()

@dataclass
class Board():
    board: List[List[bool]]
    def __hash__(self) -> int:
        exp = 1
        val = 0
        for row in self.board:
            for item in row[1:8]:
                if item:
                    val += exp
                exp *= 2
        return val
    def board_height(self):
        val = 1
        for row in reversed(self.board):
            if any(row[1:8]):
                return len(self.board) - val
            val += 1
        return 0


points = [Point(0,0), Point(1,0), Point(2, 0), Point(3, 0)]
line = Line(points)

points = [Point(1, 2), Point(0, 1), Point(1, 1), Point(2, 1), Point(1, 0)]
cross = Cross(points)

points = [Point(2, 2), Point(2, 1), Point(0, 0), Point(1, 0), Point(2, 0)]
j_shape = JShape(points)

points = [Point(0,0), Point(0,1), Point(0,2), Point(0,3)]
l_shape = LShape(points)

points = [Point(0,0), Point(1,0), Point(0, 1), Point(1, 1)]
square = Square(points)

rock_iter = infinite_iterator([line, cross, j_shape, l_shape, square])
direction_iter = infinite_iterator(input)
board = Board([[True for _ in range(9)]])
def row_gen():
    return [True, *[False for _ in range(7)], True]

def shift_down(shape: Shape):
    points = frozenset([Point(point.x, point.y-1) for point in shape.points])
    return Shape(points, Point(shape.root.x, shape.root.y-1))
def shift_left(shape: Shape):
    points = frozenset([Point(point.x-1, point.y) for point in shape.points])
    return Shape(points, Point(shape.root.x-1, shape.root.y))
def shift_right(shape: Shape):
    points = frozenset([Point(point.x+1, point.y) for point in shape.points])
    return Shape(points, Point(shape.root.x+1, shape.root.y))

def move_shape(shape: Shape, new_root: Point):
    diffy = new_root.y - shape.root.y
    diffx = new_root.x - shape.root.x
    points = frozenset([Point(point.x + diffx, point.y + diffy) for point in shape.points])
    return Shape(points, new_root)

def display_board(board: Board):
    for row in reversed(board.board):
        line = ""
        for item in row:
            if item:
                line += "#"
            else:
                line += "."
        print(line)
    print("")
    print("")
    print("")
def compare_boards(board1: Board, board2: Board):
    for i in reversed(list(range(len(board1.board)))):
        line = ""
        row1 = board1.board[i]
        row2 = board2.board[i]
        for item in row1:
            if item:
                line += "#"
            else:
                line += "."
        print("  ")
        for item in row2:
            if item:
                line += "#"
            else:
                line += "."
        print(line)
#1514285714288
#1520000000001
@functools.cache
def move_three(shape: Shape, l1:bool, l2:bool, l3:bool):
    right = max(point.x for point in shape.points)
    if l1 and shape.root.x > 1:
        shape = shift_left(shape)
        right -= 1
    elif (not l1) and right < 7:
        shape = shift_right(shape)
        right += 1
    
    if l2 and shape.root.x > 1:
        shape = shift_left(shape)
        right -= 1
    elif (not l2) and right < 7:
        shape = shift_right(shape)
        right += 1
    
    if l3 and shape.root.x > 1:
        shape = shift_left(shape)
    elif (not l3) and right < 7:
        shape = shift_right(shape)
    return shape
def clean_board(board: Board):
    val = 1
    new_board = []
    for line in reversed(board.board):
        if all(line):
            new_board.append(line)
            break
        elif any(item for item in line[1:8]):
            new_board.append(line)
        val += 1
    else:
        return board
    return Board(list(reversed(new_board)))
cycle = 5 * len(input)
cycled_boards: List[Board] = []
full_height = 0
cycle_num = 0
rock_total = 1_000_000
#rock_total =    35_000_000
#Cycle:         17_206_020
rock_num = 0
check_boards = True
empty_boards = set()
empty_board_heights: Dict[int, int] = {}
held_directions = []
cycle_target = 34_411_175
while rock_num < rock_total:
    if rock_num % 1_000 == 0 and rock_num > 0:
        print(rock_num)
    j1 = next(direction_iter) == "<"
    j2 = next(direction_iter) == "<"
    j3 = next(direction_iter) == "<"
    board_rock = move_shape(next(rock_iter), Point(3, 3))
    board_rock = move_three(board_rock, j1, j2, j3)
    height = board.board_height()
    board_rock = move_shape(board_rock, Point(board_rock.root.x, height+1))
    rock_height = max([point.y for point in board_rock.points])
    while len(board.board) <= rock_height:
        board.board.append(row_gen())
    falling = True
    dist_fallen = 0
    while(falling):
        jet = next(direction_iter)
        if jet == "<":
            next_loc = shift_left(board_rock)
        else:
            next_loc = shift_right(board_rock)
        for point in next_loc.points:
            if board.board[point.y][point.x]:
                break
        else:
            board_rock = next_loc
        next_loc = shift_down(board_rock)
        for point in next_loc.points:
            if board.board[point.y][point.x]:
                falling = False
                break
        else:
            board_rock = next_loc
        dist_fallen += 1
    for point in board_rock.points:
        board.board[point.y][point.x] = True
    rock_max = max([point.y for point in board_rock.points])
    if height < rock_max:
        full_height += rock_max - height
    y_check = list(set([point.y for point in board_rock.points]))
    y_check.sort(reverse=True)
    for y in y_check:
        if all(board.board[y]):
            board.board = board.board[y:]
            if board.board_height() == 0 and check_boards:
                jet_num = rock_num%jet_count
                if jet_num in empty_boards:
                    print(f"Cycle Found! {rock_num}")
                    check_boards = False
                    print(empty_board_heights[jet_num], full_height, rock_total, jet_num)
                    full_height = empty_board_heights[jet_num][0] + (full_height - empty_board_heights[jet_num][0])*((rock_total-empty_board_heights[jet_num][1])//(rock_num - jet_num))
                    rock_num = jet_num + ((rock_total-jet_num)//(rock_num - jet_num))*(rock_num - jet_num)
                else:
                    empty_boards.add(jet_num)
                    empty_board_heights.setdefault(jet_num, (full_height, rock_num))
            break

    
    rock_num += 1
    
#1_553_587_581_844 - low
print(full_height)
#35 mil Wrong - 54375621
#35 mil Right - 54378310
#2689