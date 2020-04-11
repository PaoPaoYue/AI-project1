import sys

import itertools
from timeit import default_timer

from util import *
from board import *
from locator import *


def solve(board):
    locator = Locator(board)
    white_size = len(board.get_white())

    for comb in locator.all_boom_combos():
        print("combs", *comb)
        cur_board = board.copy()
        paths = []
        for i, target in enumerate(comb):
                path = cur_board.find_route(target)
                if not path and white_size - len(comb) - i > 0:
                    path = cur_board.find_route(target, white_size-len(comb)-i)
                if not path:
                    print("try next comb")
                    continue
                paths.append((path,target))
                if not cur_board.get_black():
                    return paths

def main():

    board = Board()
    board.read("mytestcase/test-level-2.json")
    board.print()

    paths = solve(board)

    if not paths:
        print("failed!!!")
    else:
        print("succeed!!")
        for path, target in paths:
            get_output(path, target)
    
    

if __name__ == '__main__':
    start = default_timer()
    main()
    end = default_timer()
    print("time:", end-start)

