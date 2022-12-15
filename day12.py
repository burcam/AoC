from typing import Dict, List, Set, Tuple

def get_height(char: str):
    if char == "S":
        return ord("a")
    if char == "E":
        return ord("z")
    return ord(char)

class Point():
    x_index: int
    y_index: int
    height: int
    possible_moves: List['Point'] = []
    def __init__(self, y, x, height_char) -> None:
        self.x_index = x
        self.y_index = y
        self.height = get_height(height_char)
        self.possible_moves = []
    def find_e(self, target: 'Point', visited: Set['Point']):
        if self == target:
            return [], None
        if (self.y_index, self.x_index) in visited:
            return [], visited
        visited.add((self.y_index, self.x_index))
        return self.possible_moves, visited
    def print(self):
        print("y:", self.y_index)
        print("x:", self.x_index)
        print("    height:", self.height)
        print("    children:", [(c.y_index, c.x_index) for c in self.possible_moves])

    

with open("day12") as file:
    lines = file.readlines()
    points: Dict[Tuple, Point] = {}
    for y_index, line in enumerate(lines):
        line = line.strip()
        for x_index, char in enumerate(line):
            points.setdefault((y_index, x_index), Point(y_index, x_index, char))
    for y_index, line in enumerate(lines):
        line = line.strip()
        for x_index, char in enumerate(line):
            cur_point = points.get((y_index, x_index))

            if char == "S":
                starting_point = cur_point
            elif char == "E":
                end_point = cur_point
            if y_index > 0:
                if get_height(lines[y_index-1][x_index]) < cur_point.height + 2:
                    p = points.get((y_index-1, x_index))
                    cur_point.possible_moves.append(p)
            if x_index > 0:
                if get_height(lines[y_index][x_index-1]) < cur_point.height + 2:
                    p = points.get((y_index, x_index-1))
                    cur_point.possible_moves.append(p)
            if y_index < len(lines)-1:
                if get_height(lines[y_index+1][x_index]) < cur_point.height + 2:
                    p = points.get((y_index+1, x_index))
                    cur_point.possible_moves.append(p)
            if x_index < len(line)-1:
                if get_height(lines[y_index][x_index+1]) < cur_point.height + 2:
                    p = points.get((y_index, x_index+1))
                    cur_point.possible_moves.append(p)

    visited: Set[Tuple[int, int]] = set()
    visited.add(starting_point)
    possible_moves = [point for point in points.values() if point.height == ord("a")]
    for move in possible_moves:
        move.print()
    print(len(possible_moves))
    steps = 1
    found = False
    while possible_moves and not found:
        next_moves = set()
        for point in possible_moves:
            target_moves, visited = point.find_e(end_point, visited)
            if visited is None:
                found = True
                print(steps)
                break
            next_moves.update(target_moves)
        possible_moves = next_moves
        steps += 1
