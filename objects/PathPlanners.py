from objects.LinearADT import PriorityQueue, PriorityQueue2
import curses
import math


class Dijkstra:
    def __init__(self, board):
        self.board = board

    def search(self, start, goal, screen = None):
        '''Performs search using Djikstra's algorithm
        start: (x, y) tuple
        goal: (x, y) tuple
        '''
        costs = {}
        prevs = {}
        costs[start] = 0
        prevs[start] = None

#        pq = PriorityQueue([], [])
        pq = PriorityQueue2()
        pq.enqueue(start, costs[start])

        while not pq.isEmpty():
            cur = pq.dequeue()
            cur_x, cur_y = cur
            self.board[cur_y][cur_x] = 3 # Mark as "seen"

            if cur == goal:
                break

            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                turnCost = self.isTurn(prevs[cur], nbr) * 0.5
                cost2nbr = costs[cur] + self.getCost(cur, nbr) + turnCost
                if nbr not in costs or cost2nbr < costs[nbr]:
                    # Relax costs if cost is lower
                    self.board[nbr[1]][nbr[0]] = 4 # Mark as "frontier"
                    costs[nbr] = cost2nbr
                    prevs[nbr] = cur
                    pq.enqueue(nbr, cost2nbr) # Multiple nodes possible!
            if screen:
                self.board.draw(screen)

        # Recreate path
        path = [goal]
        i, j = goal
        while prevs[(i, j)]:
            prev = prevs[(i, j)]
            path.append(prev)
            i, j = prev
        return reversed(path)

    def getCost(self, node1, node2):
        '''Finds manhattan distance between node1 and node2
        node1: (x, y) tuple
        node2: (x, y) tuple
        '''
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    def isTurn(self, node1, node2):
        '''Finds if nodes lie on same line. If not, there's a turn'''
        if node1 is None or node2 is None:
            return 0
        if node1[0] == node2[0] or node1[1] == node2[1]:
            return 0
        return 1


class AStar:
    def __init__(self, board):
        self.board = board

    def search(self, start, goal, screen = None):
        '''Performs search using Djikstra's algorithm
        start: (x, y) tuple
        goal: (x, y) tuple
        '''
        scores = {}
        prevs = {}
        scores[start] = 0
        prevs[start] = None

#        pq = PriorityQueue([], [])
        pq = PriorityQueue2()
        pq.enqueue(start, scores[start])

        while not pq.isEmpty():
            cur = pq.dequeue()
            cur_x, cur_y = cur
            self.board[cur_y][cur_x] = 3 # Mark as "seen"

            if cur == goal:
                break

            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                cost = self.getCost(cur, nbr) + self.isTurn(prevs[cur], nbr) * 0.5
                heuristic = self.getHeuristic(nbr, goal)# + self.cross(nbr, start, goal) * 0.001
                score2nbr = scores[cur] + cost
                if nbr not in scores or score2nbr < scores[nbr]:
                    # Relax costs if cost is lower
                    self.board[nbr[1]][nbr[0]] = 4 # Mark as "frontier"
                    scores[nbr] = score2nbr
                    prevs[nbr] = cur
                    pq.enqueue(nbr, score2nbr + heuristic * 1.001) # Multiple nodes possible!
            if screen:
                self.board.draw(screen)

        # Recreate path
        path = [goal]
        i, j = goal
        while prevs[(i, j)]:
            prev = prevs[(i, j)]
            path.append(prev)
            i, j = prev
        return reversed(path)

    def getCost(self, node1, node2):
        '''Finds manhattan distance between node1 and node2
        node1: (x, y) tuple
        node2: (x, y) tuple
        '''
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    def getHeuristic(self, node1, node2):
        '''Finds manhattan distance between node1 and node2
        node1: (x, y) tuple
        node2: (x, y) tuple
        '''
        #return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])
        return (abs(node1[0] - node2[0])**2 
                + abs(node1[1] - node2[1])**2)**(1/2)

    def cross(self, node1, node2, node3):
        '''Calculates vector cross-product between node1 and node3, 
        and current node2 to node3. Used for heuristic calculation
        Typically, node1 = current, node2 = start, node3 = goal
        '''
        dx1 = node1[0] - node3[0]
        dy1 = node1[1] - node3[1]
        dx2 = node2[0] - node3[0]
        dy2 = node2[1] - node3[1]
        return abs(dx1*dy2 - dx2*dy1)

    def isTurn(self, node1, node2):
        '''Finds if nodes lie on same line. If not, there's a turn'''
        if node1 is None or node2 is None:
            return 0

        if node1[0] == node2[0] or node1[1] == node2[1]:
            return 0
        return 1
