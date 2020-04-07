import sys
import json
import itertools
from timeit import default_timer

from util import *
from search import AStar
from board import *
from search.PriorityQueue import *
from search.Locator import *


def main():
    with open("mytestcase/test-level-4.json") as file:
        data = json.load(file)
    print(data)

    board = Board(data["white"], data["black"])

    locator = Locator(data)
    # print(locator.find_all_boom_combos())

    for combs in locator.find_all_boom_combos():
        print("combs", combs)
        try:
            for comb in range(len(combs)):
                target = Pos(combs[comb][0], combs[comb][1])
                print("target", target)
                path = board.find_route(board.get_white(), target)
                board.rerrange_white(target)
                # print("white:")
                # for i in board.get_white():
                #     print(i[0])
                # break

            print("\n目的地的坐标:", combs)
            break
        except:
            continue

    # # 如果只有一颗白棋的情况
    # if board.get_white_size() < 2:
    #     result = []; cost = -1
    #     for i in boom_dict:
    #         try:
    #             board.find_route(board.get_white(), Pos(i[0], i[1]))
    #             board.update_zone()
    #             return
    #         except:
    #             continue
    # # 有2，3颗白棋
    # else:
    #
    # # if next(boom_dict)
    # #     for size in board.get_white_size():
    #     for combs in itertools.combinations(boom_dict, board.get_white_size()):
    #         print("combs", combs)
    #         partial_arr = []
    #         if any_lst1_in_lst2(combs, black_without_n):
    #             continue
    #         for comb in combs:
    #             partial_arr += boom(([], []), [comb[0], comb[1]], [], black_without_n)[0]
    #
    #         # if all black will be boomed
    #         if all_lst1_in_lst2(black_without_n, partial_arr):
    #             try:
    #                 for comb in combs:
    #                     board.find_route(board.get_white(), Pos(comb[0], comb[1]))
    #                     # board.get_white().remove((Pos(comb[0], comb[1]), 1))
    #                     # board.update_zone()
    #                 print("\n目的地的坐标:", combs)
    #                 return
    #             except:
    #                 continue

                # for point in partial_white:
                #     for
                #     try:
                #         AStar.AStarSearch(point)
                #
                # setdiff_between_lists(partial_white, combs)
                # print("partial white:", partial_white)
                #
                # try:
                #     for point in range(len(partial_white)):
                #         start = partial_white[0]
                #         end = (0, combs[point][0], combs[point][1])
                #         result, cost = AStar.AStarSearch(start, end, graph)
                #         show_output(result, cost, graph)
                #     return
                # except:
                #     continue
    

if __name__ == '__main__':
    start = default_timer()
    main()
    end = default_timer()
    print("time:", end-start)

