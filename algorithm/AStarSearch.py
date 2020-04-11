from algorithm.PriorityQueue import *

class Node:
    
    def __init__(self, prev, cost):
        self.prev = prev
        self.cost = cost

    def cameFrom(self):
        return self.prev

    def priority(self):
        return self.heuristic() + self.cost

    def heuristic(self):
        pass

    def neighbours(self):
        pass

    def __hash__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        else:
            return False

    def __lt__(self, other):
        pass



def AStarSearch(start, goal_test):

    closedVertices = []
    openVertices = IndexQueue()

    openVertices.push(hash(start), start)

    while not openVertices.empty():
        # Get the vertex in the open list with the lowest F score
        current = openVertices.pop()

        # Check if we have reached the goal
        if goal_test(current):
            # Retrace our route backward
            path = [current]
            while current.cameFrom():
                current = current.cameFrom()
                path.append(current)
            path.reverse()
            return path  # Done!

        closedVertices.append(current)

        # Update scores for vertices near the current position
        for neighbour in current.neighbours():
            # We have already processed this node exhaustively
            if neighbour in closedVertices:
                continue

            hashKey = hash(neighbour)
            # Discovered a new vertex
            if not openVertices.contain(hashKey):
                openVertices.push(hashKey, neighbour)            
            # Update scores for vertices in the open list
            elif openVertices.get(hashKey).priority() < neighbour.priority():
                openVertices.change(hashKey, neighbour)

    return []
