from __future__ import print_function
import matplotlib.pyplot as plt


class AStarGraph(object):
    # Define a class board like grid with two barriers

    def __init__(self, arr):
        self.barriers = arr
        print("barriers", self.barriers)

    def heuristic(self, start, goal):
        # Use Manhattan Distance as heuristic
        return abs(start[1]-goal[1]) + abs(start[2]-goal[2])

    def neighbours(self, pos):
        n = []
        # Moves allow link a chess king
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x2 = pos[1] + dx
            y2 = pos[2] + dy
            if x2 < 0 or x2 > 8 or y2 < 0 or y2 > 8:
                continue
            canpass = True
            for barrier in self.barriers:
                if x2 == barrier[1] and y2 == barrier[2]:
                    for opposite in self.barriers:
                        if x2+dx == opposite[1] and y2+dy == opposite[2]:
                            canpass = False
                            break
                    if canpass:
                        x2 += dx
                        y2 += dy
                    break
            if canpass:
                n.append((pos[0], x2, y2))
        return n

    def move_cost(self, a, b):
        for barrier in self.barriers:
            if b in barrier and b[0] > barrier[0]:
                return 100  # Extremely high cost to enter barrier squares
        return 1  # Normal movement cost


def AStarSearch(start, end, graph):
    G = {}  # Actual movement cost to each position from the start position
    F = {}  # Estimated movement cost of start to end going via this position

    # Initialize starting values
    G[start] = 0
    F[start] = graph.heuristic(start, end)

    closedVertices = set()
    openVertices = set([start])
    cameFrom = {}

    while len(openVertices) > 0:
        # Get the vertex in the open list with the lowest F score
        current = None
        currentFscore = None
        for pos in openVertices:
            if current is None or F[pos] < currentFscore:
                currentFscore = F[pos]
                current = pos

        # Check if we have reached the goal
        if current[1:] == end[1:]:
            # Retrace our route backward
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return path, F[current]  # Done!

        # Mark the current vertex as closed
        openVertices.remove(current)
        closedVertices.add(current)

        # Update scores for vertices near the current position
        for neighbour in graph.neighbours(current):
            if neighbour in closedVertices:
                continue  # We have already processed this node exhaustively
            candidateG = G[current] + graph.move_cost(current, neighbour)

            if neighbour not in openVertices:
                openVertices.add(neighbour)  # Discovered a new vertex
            elif candidateG >= G[neighbour]:
                continue  # This G score is worse than previously found

            # Adopt this G score
            cameFrom[neighbour] = current
            G[neighbour] = candidateG
            H = graph.heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + H

    raise RuntimeError("A* failed to find a solution")

