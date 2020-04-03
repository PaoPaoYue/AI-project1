import sys
import json

from search.util import print_move, print_boom, print_board
from search import AStar


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # Process data
    print(data)
    white = data['white']
    black = data['black']

    graph = AStar.AStarGraph(black)
    result, cost = AStar.AStarSearch(tuple(white[0][1:]), tuple(black[0][1:]), graph)


    print("route", result)
    print("cost", cost)
    AStar.plt.plot([v[0] for v in result], [v[1] for v in result])
    for barrier in graph.barriers:
        AStar.plt.plot([v[0] for v in barrier], [v[1] for v in barrier])
    AStar.plt.xlim(0, 8)
    AStar.plt.ylim(0, 8)
    AStar.plt.show()


if __name__ == '__main__':
    main()

