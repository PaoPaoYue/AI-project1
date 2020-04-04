import sys
import json

from search.util import print_move, print_boom, print_board, sort_by_values_len, print_dict
from search import AStar


# Take an empty array, a point and all enemies, check if the white boom here, how many black can be killed
# WARN: This function can not detect the white yet
# the parameter copy is to prevent data loss
def boom(arr, point, copy, black):
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            neighbour = [point[0]+i, point[1]+j]
            if neighbour[0] < 0 or neighbour[0] > 8 or neighbour[1] < 0 or neighbour[1] > 8:
                continue
            arr[1].append(neighbour)
            if (neighbour in black) and (neighbour not in copy):
                arr[0].append(neighbour)
                copy.append(neighbour)
                boom(arr, neighbour, copy, black)
    return arr


# 找到能炸的最多的点并排序
def most_valuable_points(black_without_n):
    boom_dict = {}
    for i in range(0, 9):
        for j in range(0, 9):
            if [i, j] in black_without_n:
                continue
            boom_dict[(i, j)] = boom(([], []), [i, j], [], black_without_n)
    # sort the dict by value in descending order
    return sort_by_values_len(boom_dict)


# 这一部分是看outout的 matplot部分最后需要删掉
def show_output(result, cost, graph):
    print("route", result)
    print("cost", cost)
    AStar.plt.plot([v[1] for v in result], [v[2] for v in result])
    for barrier in graph.barriers:
        if barrier in result:
            print("There is an error in point", barrier)
    AStar.plt.xlim(0, 8)
    AStar.plt.ylim(0, 8)
    AStar.plt.show()

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # Process data
    print(data)
    white = data['white']
    black = data['black']
    black_without_n = [i[1:] for i in black]
    print(black_without_n)

    # graph就是路障所处的位置(白棋不算路障)
    graph = AStar.AStarGraph(black)

    # start就是我们选中的白棋子
    start = (1,0,0)
    # end就是需要定义我们想让白棋子走到哪个点的坐标
    end = (0,7,1)

    # 打印字典 列出所有点炸的结果 value里第一个list列出所有能炸到黑点 第二个列出所有能炸到的点
    print_dict(most_valuable_points(black_without_n))
    result, cost = AStar.AStarSearch(start, end, graph)

    show_output(result, cost, graph)


if __name__ == '__main__':
    main()

