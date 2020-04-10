import sys

import itertools
from timeit import default_timer

from util import *
from board import *
from locator import *


def main():

    board = Board()
    board.read("mytestcase/test-level-3.json")
    board.print()

    locator = Locator(board)
    white_size = len(board.get_white())
    for comb in locator.all_boom_combos():
        print("combs", *comb)
        cur_board = board.copy()
        path = []
        for i, pos in enumerate(comb):
                path = cur_board.find_route(pos)
                if not path and white_size - len(comb) - i > 0:
                    path = cur_board.find_route(pos, white_size-len(comb)-i)
                if not path:
                    print("try next comb")
                    continue
                if i == len(comb) - 1:
                    print("succeed!!")
                    return
    

if __name__ == '__main__':
    start = default_timer()
    main()
    end = default_timer()
    print("time:", end-start)

