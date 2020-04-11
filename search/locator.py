# The class to locate the boom destinations. Give white tokens positions to boom all black

import itertools

from search.board import *


class Locator:

    def __init__(self, board):
        self.board = board
        self.white = board.get_white()
        self.black = board.get_black()
        self.boom_dict = self.__create_boom_dict()

    def __no_equal_set(self, sets):
        for i, set in enumerate(sets):
            for j, other_set in enumerate(sets):
                if i != j and set == other_set:
                    return False
        return True

    # find the closest distance between any white token and the destination
    def __closest_dist(self, target):
        min_dist = BOARD_LEN * BOARD_LEN
        for pos,_ in self.white:
            dist = target.manh_dist(pos)
            if dist < min_dist:
                min_dist = dist
        return min_dist

    # create a dictionary that contains all points
    # store the result that which cells will be explored when a white token boom at this point.
    def __create_boom_dict(self):
        boom_dict = {}
        for x in range(BOARD_LEN):
            for y in range(BOARD_LEN):
                pos = Pos(x, y)
                if self.board.get_p(pos).chess == Chess.black:
                    continue
                boom_set = self.board.get_boom(pos, True)
                if boom_set:
                    boom_dict[pos] = boom_set
        return boom_dict

    # find all possible combos of points that can boom all black tokens
    def all_boom_combos(self):
        white_size = sum([num for pos, num in self.white])
        black_size = len(self.black)
        combos = []
        for i in range(white_size, 0, -1):
            for comb in itertools.combinations(self.boom_dict.items(), i):
                if self.__no_equal_set([boom_set for pos, boom_set in comb]):
                    all_boom_set = set()
                    pos_comb = []
                    for pos, boom_set in comb:
                        pos_comb.append(pos)
                        all_boom_set.update(boom_set)
                    if len(all_boom_set) == black_size:
                        for res in itertools.permutations(pos_comb, len(pos_comb)):
                            combos.append(res)
        # sort it to make the one who can boom the largest number of enemies at the top
        return sorted(combos, key=lambda combo: sum(self.__closest_dist(pos) for pos in combo))

