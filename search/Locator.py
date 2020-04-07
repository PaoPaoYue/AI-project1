import operator
from util import *
import itertools


class Locator:

    def __init__(self, data):
        self.size = sum([i[0] for i in data['white']])
        self.barriers = [(i[1], i[2]) for i in data['black']]
        self.white = [((i[1], i[2]), i[0]) for i in data['white']]
        self.boom_dict = self.create_boom_dict()


    def create_boom_dict(self):
        boom_dict = {}
        for i in range(0, 9):
            for j in range(0, 9):
                if (i, j) in self.barriers:
                    continue
                boom_dict[(i, j)] = boom(self, ([], []), (i, j), [])

        # sort the dict by value in descending order
        return sort_by_values_len(boom_dict, True)

    def find_all_boom_combos(self):
        boom_points = []
        for comb in self.boom_dict:
            partial_arr = []
            if any_lst1_in_lst2(comb, self.barriers):
                continue

            partial_arr += boom(self, ([], []), [comb[0], comb[1]], [])[0]
            if all_lst1_in_lst2(self.barriers, partial_arr):
                boom_points.append(comb)
                continue
            break

        for size in range(2, self.size+1):
            for combs in itertools.combinations(self.boom_dict, size):
                partial_arr = []
                if any_lst1_in_lst2(combs, self.barriers):
                    continue
                for comb in combs:
                    partial_arr += boom(self, ([], []), [comb[0], comb[1]], [])[0]

                # if all black will be boomed
                if all_lst1_in_lst2(self.barriers, partial_arr):
                    boom_points.append(combs)
        # for i in boom_points:
        #     print(i)
        return boom_points


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
