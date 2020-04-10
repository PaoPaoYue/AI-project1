import operator
import itertools

from util import *
from board import *


class Locator:

    def __init__(self, board):
        self.board = board
        self.white = board.get_white()
        self.black = board.get_black()
        self.boom_dict = self.__create_boom_dict()

    def __closest_dist(self, target):
        min_dist = BOARD_LEN * BOARD_LEN
        for pos,_ in self.white:
            dist = target.manh_dist(pos)
            if dist < min_dist:
                min_dist = dist
        return min_dist


    def __create_boom_dict(self):
        boom_dict = {}
        for x in range(BOARD_LEN):
            for y in range(BOARD_LEN):
                pos = Pos(x, y)
                if self.board.get_p(pos).chess == Chess.black:
                    continue
                boom_set = self.board.get_boom(pos, True)
                if boom_set:
                    boom_tuple = tuple(sorted(boom_set))
                    if boom_tuple in boom_dict:
                        if self.__closest_dist(pos) < self.__closest_dist(boom_dict[boom_tuple]):
                            boom_dict[boom_tuple] = pos
                    else:
                        boom_dict[boom_tuple] = pos
        for boom_set, pos in boom_dict.items():
            print(*boom_set, "pos::", pos)
        return boom_dict

    def all_boom_combos(self):
        white_size = sum([num for pos, num in self.white])
        black_size = len(self.black)
        for i in range(white_size, 0, -1):
            for comb in itertools.combinations(self.boom_dict.items(), i):
                all_boom_set = set()
                pos_comb = []
                for boom_set, pos in comb:
                    pos_comb.append(pos)
                    all_boom_set.update(boom_set)
                if len(all_boom_set) == black_size:
                    for res in itertools.permutations(pos_comb, len(pos_comb)):
                        yield res


# 根据能炸到的黑点的个数排倒序 只输出可炸点
def sort_by_values_len(dictionary, need_reverse):

    dict_len = {key: len(value[0]) for key, value in dictionary.items()}
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=need_reverse)
    sorted_dict = {item[0]: dictionary[item[0]] for item in sorted_key_list if len(dictionary[item[0]][0]) > 0}
    return sorted_dict


# Take an empty array, a start point and all enemies, check if the white boom here, how many black can be killed
# WARN: This function can not detect the white yet
# the parameter copy is to prevent data loss
def boom(self, arr, start, copy):

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            neighbour = (start[0] + i, start[1] + j)
            if neighbour[0] < 0 or neighbour[0] > 8 or neighbour[1] < 0 or neighbour[1] > 8:
                continue
            arr[1].append(neighbour)

            if (neighbour in self.barriers) and (neighbour not in copy):
                arr[0].append(neighbour)
                copy.append(neighbour)
                boom(self, arr, neighbour, copy)
    return arr
