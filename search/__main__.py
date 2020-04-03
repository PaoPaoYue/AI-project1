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

    # graph就是路障所处的位置(只考虑了黑棋为路障的情况) 我还没有考虑n 所以现在只要有路障就跳不过去
    graph = AStar.AStarGraph(black)

    # start就是我们选中的白棋子
    start = (1,0,0)
    # end就是需要定义我们想让白棋子走到哪个点的坐标
    end = (0,7,1)
    result, cost = AStar.AStarSearch(start, end, graph)

    # 这一部分是看outout的 matplot部分最后需要删掉
    print("route", result)
    print("cost", cost)
    AStar.plt.plot([v[1] for v in result], [v[2] for v in result])
    for barrier in graph.barriers:
        if barrier in result:
            print("There is an error in point", barrier)
    AStar.plt.xlim(0, 8)
    AStar.plt.ylim(0, 8)
    AStar.plt.show()


if __name__ == '__main__':
    main()

