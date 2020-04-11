"""
The main module of project part A. This project aims to boom all black tokens out by moving the white ones.
We'll control no more than three white tokens to deal with that one
"""

import sys
from timeit import default_timer
from search.locator import *


# Find the solution
def solve(board):
    locator = Locator(board)
    white_size = len(board.get_white())

    # Try every combinations of the destinations
    for combo in locator.all_boom_combos():
        print("# try combo", *combo)
        cur_board = board.copy()
        paths = []
        for i, target in enumerate(combo):
            path = cur_board.find_route(target)
            if not path and white_size - len(combo) - i > 0:
                path = cur_board.find_route(target, white_size-len(combo)-i)
            if not path:
                break
            paths.append((path, target))
            if not cur_board.get_black():
                return paths    # Done!

def main():

    board = Board()
    board.read(sys.argv[1])
    board.print()

    # Try to fin a path
    paths = solve(board)

    if not paths:
        print("failed!!!", file=sys.stderr)
    else:
        # If there is a path, print it!
        for path, target in paths:
            get_output(path, target)
    


if __name__ == '__main__':
    start = default_timer()
    main()
    end = default_timer()
    print("# time used: {}s".format(end-start))

