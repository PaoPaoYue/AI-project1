import json
from enum import Enum
from collections import defaultdict

from util import *
from search.AStarSearch import *

BOARD_LEN = 8


class Chess(Enum):
    none = 0
    white = 1
    black = 2


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def off_board(self):
        return self.x < 0 or self.x >= BOARD_LEN or self.y < 0 or self.y >= BOARD_LEN

    def neighbour(self):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new = Pos(self.x + dx, self.y + dy)
                if (not (new == self or new.off_board())):
                    yield new

    def card_neighbour(self, distance):
        for dx in range(-distance, distance + 1):
            new_x = self.x + dx
            if (dx != 0 and new_x >= 0 and new_x < BOARD_LEN):
                yield Pos(new_x, self.y)

        for dy in range(-distance, distance + 1):
            new_y = self.y + dy
            if (dy != 0 and new_y >= 0 and new_y < BOARD_LEN):
                yield Pos(self.x, new_y)

    def manh_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        else:
            return False

    def __hash__(self):
        return self.x + self.y * BOARD_LEN

    def __str__(self):
        return str((self.x, self.y))


class Cell:

    def __init__(self, x, y):
        self.pos = Pos(x, y)
        self.chess = Chess.none
        self.num = 0
        self.zone = 0
    
    def copy(self):
        new = Cell(self.pos.x, self.pos.y)
        new.chess = self.chess
        new.num = self.num
        new.zone = self.zone
        return new


class Board:

    def __init__(self):
        self.cells = []               

    def read(self, filename):
        self.cells = [Cell(i % BOARD_LEN, i // BOARD_LEN) for i in range(BOARD_LEN ** 2)]
        with open(filename) as file:
            data = json.load(file)
        for pieces in data["white"]:
            self.get(pieces[1], pieces[2]).num = pieces[0]
            self.get(pieces[1], pieces[2]).chess = Chess.white
        for pieces in data["black"]:
            self.get(pieces[1], pieces[2]).num = pieces[0]
            self.get(pieces[1], pieces[2]).chess = Chess.black
        self.__update_zone()

    def copy(self):
        new = Board()
        new.cells = [cell.copy() for cell in self.cells]
        return new

    def get(self, x, y):
        return self.cells[y * BOARD_LEN + x]

    def get_p(self, pos):
        return self.cells[pos.y * BOARD_LEN + pos.x]

    def get_white(self):
        return [(cell.pos, cell.num) for cell in self.cells if cell.chess == Chess.white]

    def get_black(self):
        return [(cell.pos, cell.num) for cell in self.cells if cell.chess == Chess.black]

    def get_boom(self, start, black_only):
        mark = defaultdict(bool)
        queue = [start]
        boom = set()
        if not black_only:
            boom.add(start)
        while queue:
            pos = queue.pop()
            mark[pos] = True
            for neighbour in Pos(pos.x, pos.y).neighbour():
                if not mark[neighbour]:
                    if self.get_p(neighbour).chess == Chess.black:
                        queue.append(neighbour)
                        if black_only:
                            boom.add(neighbour)
                    if not black_only:
                        boom.add(neighbour)
        return boom

    def set_white(self, white):
        for cell in self.cells:
            if cell.chess == Chess.white:
                cell.num = 0
                cell.chess = Chess.none
        for pos, num in white:
            cell = self.get_p(pos)
            cell.num = num
            cell.chess = Chess.white

    def set_boom(self, target):
        boom = self.get_boom(target, False)
        for pos in boom:
            cell = self.get_p(pos)
            cell.num = 0
            cell.chess = Chess.none
        self.__update_zone()
    

    def find_route(self, target, ignore =0):
        board = self

        class BoardNode(Node):
            def __init__(self, white, cost, prev):
                super().__init__(prev, cost)
                self.white = sorted(white)
                self.cost = cost

            def heuristic(self):
                target_zone = board.get_p(target).zone
                in_score = []
                out_score = []
                for pos, num in self.white:
                    dist = pos.manh_dist(target) * num
                    if board.get_p(pos).zone == target_zone:
                        in_score.append(dist)
                    else:
                        out_score.append(dist)
                if in_score:
                    return sum(in_score)
                else:
                    return sum(out_score)

            def neighbours(self):
                for selected_pos, _ in self.white:
                    old = []
                    new = []
                    for pos, num in self.white:
                        if not selected_pos == pos:
                            old.append((pos, num))
                        else:
                            for neighbour in pos.card_neighbour(num):
                                if board.get_p(neighbour).chess != Chess.black:
                                    for i in range(num):
                                        cur = [(neighbour, num - i)]
                                        if (i != 0):
                                            cur.append((pos, i))
                                        new.append(cur)
                    for new_stacks in new:
                        res = defaultdict(int)
                        for pos, num in old:
                            res[pos] += num
                        for pos, num in new_stacks:
                            res[pos] += num
                        yield BoardNode(res.items(), self.cost + 1, self)

            def __hash__(self):
                return hash(tuple(self.white))

            def __lt__(self, other):
                return self.priority() < other.priority()

            def __str__(self):
                return ','.join(['({}, {})'.format(str(pos), num) for pos, num in self.white]) + str(self.priority())
               
        def goal_test():
            boom = self.get_boom(target, False)

            def __inner(node):
                get_target = False
                in_boom_num = 0
                for pos, num in node.white:
                    if pos == target:
                        get_target = True
                    if pos in boom:
                        in_boom_num += num
                return get_target and in_boom_num <= (ignore + 1)

            return __inner

        print("search starts! ignore:" , ignore)
        path = AStarSearch(BoardNode(board.get_white(), 0, None), goal_test())
        if path:
            print("result:")
            for node in path:
                board.set_white(node.white)
                board.print()
            board.set_boom(target)
            board.print()
        else:
            print("failed to find route")
        return path

    def print(self):
        print_dict = {}
        for cell in self.cells:
            if cell.chess == Chess.black:
                print_dict[(cell.pos.x, cell.pos.y)] = "x" * cell.num
            elif cell.chess == Chess.white:
                print_dict[(cell.pos.x, cell.pos.y)] = "o" * cell.num
            else:
                print_dict[(cell.pos.x, cell.pos.y)] = ""
        print_board(print_dict, "Board status", True)

    def print_zone(self):
        print_dict = {}
        for cell in self.cells:
            if cell.chess == Chess.black:
                print_dict[(cell.pos.x, cell.pos.y)] = "x"
            elif cell.chess == Chess.white:
                print_dict[(cell.pos.x, cell.pos.y)] = "o " + str(cell.zone)
            else:
                print_dict[(cell.pos.x, cell.pos.y)] = cell.zone
        print_board(print_dict, "Board zone status", True)

    def __update_zone(self):
        zone = 1
        mark = defaultdict(bool)
        queue = []

        for x in range(BOARD_LEN):
            for y in range(BOARD_LEN):
                start = Pos(x, y)
                if (mark[start] or self.get_p(start).chess == Chess.black):
                    continue

                queue.append(start)
                while queue:
                    pos = queue.pop()
                    mark[pos] = True

                    self.get_p(pos).zone = zone

                    for neighbour in Pos(pos.x, pos.y).card_neighbour(1):
                        if not mark[neighbour] and self.get_p(neighbour).chess != Chess.black:
                            queue.append(neighbour)

                zone += 1




