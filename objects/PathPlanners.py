from objects.LinearADT import PriorityQueue, PriorityQueue2
import curses
import math


class Dijkstra:
    def __init__(self, board, mode_c, mode_h):
        self.board = board
        self.mode_c = mode_c
        self.mode_h = mode_h

    def search(self, start, goal, screen = None):
        '''Performs search using Dijkstra's algorithm
        Animates screen if screen is provided
        start: (x, y) tuple
        goal: (x, y) tuple
        '''
        costs = {}
        prevs = {}
        costs[start] = 0
        prevs[start] = None

        pq = PriorityQueue2()
        pq.enqueue(start, costs[start])

        while not pq.isEmpty():
            cur = pq.dequeue()
            cur_x, cur_y = cur

            self.board[cur_y][cur_x] = 3 # Mark as "seen"
            if screen:
                self.board.draw_cell(cur_x, cur_y, screen)
                self.board.draw_player(screen)

            if cur == goal:
                break

            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                turnCost = self.isTurn(prevs[cur], nbr) * 0.2
                cost2nbr = costs[cur] + self.getCost(cur, nbr, self.mode_c) + turnCost
                if nbr not in costs or cost2nbr < costs[nbr]:
                    # Mark as frontier
                    self.board[nbr[1]][nbr[0]] = 4 

                    if screen:
                        self.board.draw_cell(nbr[0], nbr[1], screen)

                    # Relax costs if cost is lower
                    costs[nbr] = cost2nbr
                    prevs[nbr] = cur
                    pq.enqueue(nbr, cost2nbr) # Multiple nodes possible!
            if screen:
                self.board.draw_player(screen)
                self.board.draw_goal(screen)
                screen.refresh()

        # Recreate path
        path = [goal]
        i, j = goal
        while prevs[(i, j)]:
            prev = prevs[(i, j)]
            path.append(prev)
            i, j = prev
        return reversed(path)

    def getCost(self, node1, node2, mode = 0):
        '''Finds distance between node1 and node2
        node1: (x, y) tuple
        node2: (x, y) tuple
        mode: 0 - Manhattan, 1 - Euclidean
        '''
        if mode == 0:
            return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])
        elif mode == 1:
            return (abs(node1[0] - node2[0])**2 
                    + abs(node1[1] - node2[1])**2)**(1/2)

    def isTurn(self, node1, node2):
        '''Finds if nodes lie on same line. If not, there's a turn'''
        if node1 is None or node2 is None:
            return 0
        if node1[0] == node2[0] or node1[1] == node2[1]:
            return 0
        return 1

class AStar(Dijkstra):
    def search(self, start, goal, screen = None):
        '''Performs search using AStar algorithm
        Animates screen if screen is provided
        start: (x, y) tuple
        goal: (x, y) tuple
        '''
        scores = {}
        prevs = {}
        scores[start] = 0
        prevs[start] = None

        pq = PriorityQueue2()
        pq.enqueue(start, scores[start])

        while not pq.isEmpty():
            cur = pq.dequeue()
            cur_x, cur_y = cur

            # Mark as seen
            self.board[cur_y][cur_x] = 3
            if screen:
                self.board.draw_cell(cur_x, cur_y, screen)
                self.board.draw_player(screen)

            if cur == goal: 
                break 

            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                cost = (self.getCost(cur, nbr, self.mode_c) + self.isTurn(prevs[cur], nbr) * 0.2)
                heuristic = (self.getHeuristic(nbr, goal, self.mode_h))
                score2nbr = scores[cur] + cost
                if nbr not in scores or score2nbr < scores[nbr]:
                    # Mark as "frontier"
                    self.board[nbr[1]][nbr[0]] = 4
                    if screen:
                        self.board.draw_cell(nbr[0], nbr[1], screen)

                    # Relax costs
                    scores[nbr] = score2nbr
                    prevs[nbr] = cur
                    pq.enqueue(nbr, score2nbr + heuristic * 0.999) # Multiple nodes possible!
            if screen:
                self.board.draw_player(screen)
                self.board.draw_goal(screen)
                screen.refresh()

        # Recreate path
        path = [goal]
        i, j = goal
        while prevs[(i, j)]:
            prev = prevs[(i, j)]
            path.append(prev)
            i, j = prev
        return reversed(path)

    def getHeuristic(self, node1, node2, mode = 0):
        '''Finds manhattan distance between node1 and node2
        node1: (x, y) tuple
        node2: (x, y) tuple
        mode: 0 - Manhattan, 1 - Euclidean
        '''
        if mode == 0:
            return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])
        elif mode == 1:
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


class Greedy(AStar):
    def search(self, start, goal, screen = None):
        '''Performs greedy search
        Animates screen if screen is provided
        start: (x, y) tuple
        goal: (x, y) tuple
        '''
        scores = {}
        prevs = {}
        scores[start] = 0
        prevs[start] = None

        pq = PriorityQueue2()
        pq.enqueue(start, scores[start])

        while not pq.isEmpty():
            cur = pq.dequeue()
            cur_x, cur_y = cur

            self.board[cur_y][cur_x] = 3 # Mark as "seen"
            if screen:
                self.board.draw_cell(cur_x, cur_y, screen)

            if cur == goal:
                break

            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                cost = self.getCost(cur, nbr, self.mode_c) + self.isTurn(prevs[cur], nbr)
                heuristic = self.getHeuristic(nbr, goal, self.mode_h)
                score2nbr = scores[cur] + cost
                if nbr not in scores or score2nbr < scores[nbr]:
                    # Mark as frontier
                    self.board[nbr[1]][nbr[0]] = 4
                    if screen:
                        self.board.draw_cell(nbr[0], nbr[1], screen)
                    
                    # Relax costs if cost is lower
                    scores[nbr] = score2nbr
                    prevs[nbr] = cur
                    pq.enqueue(nbr, heuristic) # Multiple nodes possible!
            if screen:
                self.board.draw_player(screen)
                self.board.draw_goal(screen)
                screen.refresh()

        # Recreate path
        path = [goal]
        i, j = goal
        while prevs[(i, j)]:
            prev = prevs[(i, j)]
            path.append(prev)
            i, j = prev
        return reversed(path)


class DijkstraBD(Dijkstra):
    def search(self, start, goal, screen = None):
        '''Performs search using Dijkstra's algorithm
        Animates screen if screen is provided
        start: (x, y) tuple
        goal: (x, y) tuple
        '''
        costs_s = {}
        prevs_s = {}
        costs_s[start] = 0
        prevs_s[start] = None

        costs_g = {}
        prevs_g = {}
        costs_g[goal] = 0
        prevs_g[goal] = None

        pq_s = PriorityQueue2()
        pq_s.enqueue(start, costs_s[start])

        pq_g = PriorityQueue2()
        pq_g.enqueue(goal, costs_g[goal])

        while not pq_s.isEmpty() and not pq_g.isEmpty():
            cur = pq_s.dequeue()
            cur_x, cur_y = cur

            # Mark as seen
            self.board[cur_y][cur_x] = 3
            if screen:
                 self.board.draw_cell(cur_x, cur_y, screen)

            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                turnCost = self.isTurn(prevs_s[cur], nbr) * 0.2
                cost2nbr = costs_s[cur] + self.getCost(cur, nbr, self.mode_c) + turnCost
                if nbr not in costs_s or cost2nbr < costs_s[nbr]:
                    # Mark as frontier
                    self.board[nbr[1]][nbr[0]] = 4 
                    if screen:
                        self.board.draw_cell(nbr[0], nbr[1], screen)

                    # Relax costs if cost is lower
                    costs_s[nbr] = cost2nbr
                    prevs_s[nbr] = cur
                    pq_s.enqueue(nbr, cost2nbr) # Multiple nodes possible!

            cur = pq_g.dequeue()
            cur_x, cur_y = cur

            # Mark as seen
            self.board[cur_y][cur_x] = 3
            if screen:
                self.board.draw_cell(cur_x, cur_y, screen)

            if cur in costs_s:
                break

            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                turnCost = self.isTurn(prevs_g[cur], nbr) * 0.2
                cost2nbr = costs_g[cur] + self.getCost(cur, nbr, self.mode_c) + turnCost
                if nbr not in costs_g or cost2nbr < costs_g[nbr]:
                    # Mark as frontier
                    self.board[nbr[1]][nbr[0]] = 4
                    if screen:
                        self.board.draw_cell(nbr[0], nbr[1], screen)

                    # Relax costs
                    costs_g[nbr] = cost2nbr
                    prevs_g[nbr] = cur
                    pq_g.enqueue(nbr, cost2nbr) # Multiple nodes possible!

            if screen:
                self.board.draw_player(screen)
                self.board.draw_goal(screen)
                screen.refresh()

        # Recreate path
        path = [cur]
        i, j = cur
        while prevs_s[(i, j)]:
            prev = prevs_s[(i, j)]
            path.append(prev)
            i, j = prev
        path = list(reversed(path))

        i, j = cur
        while prevs_g[(i, j)]:
            prev = prevs_g[(i, j)]
            path.append(prev)
            i, j = prev
        return path

class AStarBD(AStar):
    def search(self, start, goal, screen = None):
        '''Performs bidirectional search using AStar algorithm
        Animates screen if screen is provided
        start: (x, y) tuple
        goal: (x, y) tuple
        screen: curses.window object
        '''
        costs_s = {}
        prevs_s = {}
        costs_s[start] = 0
        prevs_s[start] = None

        costs_g = {}
        prevs_g = {}
        costs_g[goal] = 0
        prevs_g[goal] = None

        pq_s = PriorityQueue2()
        pq_s.enqueue(start, costs_s[start])

        pq_g = PriorityQueue2()
        pq_g.enqueue(goal, costs_g[goal])

        while not pq_s.isEmpty() and not pq_g.isEmpty():
            cur = pq_s.dequeue()
            cur_x, cur_y = cur

            # Mark as seen
            self.board[cur_y][cur_x] = 3
            if screen:
                self.board.draw_cell(cur_x, cur_y, screen)

            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                turnCost = self.isTurn(prevs_s[cur], nbr) * 0.2
                cost2nbr = costs_s[cur] + self.getCost(cur, nbr, self.mode_c) + turnCost
                heuristic = self.getHeuristic(nbr, goal, self.mode_h)
                if nbr not in costs_s or cost2nbr < costs_s[nbr]:
                    # Mark as frontier
                    self.board[nbr[1]][nbr[0]] = 4
                    if screen:
                        self.board.draw_cell(nbr[0], nbr[1], screen)
                    
                    # Relax costs if cost is lower
                    costs_s[nbr] = cost2nbr
                    prevs_s[nbr] = cur
                    pq_s.enqueue(nbr, cost2nbr + heuristic * 0.999) # Multiple nodes possible!

            cur = pq_g.dequeue()
            cur_x, cur_y = cur

            self.board[cur_y][cur_x] = 3 # Mark as "seen"
            if screen:
                self.board.draw_cell(cur_x, cur_y, screen)

            if cur in costs_s:
                break

            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                turnCost = self.isTurn(prevs_g[cur], nbr) * 0.2
                cost2nbr = costs_g[cur] + self.getCost(cur, nbr, self.mode_c) + turnCost
                heuristic = self.getHeuristic(nbr, start, self.mode_h)
                if nbr not in costs_g or cost2nbr < costs_g[nbr]:
                    self.board[nbr[1]][nbr[0]] = 4 # Mark as "frontier"
                    if screen:
                        self.board.draw_cell(nbr[0], nbr[1], screen)

                    # Relax costs
                    costs_g[nbr] = cost2nbr
                    prevs_g[nbr] = cur
                    pq_g.enqueue(nbr, cost2nbr + heuristic * 0.999) # Multiple nodes possible!

            if screen:
                self.board.draw_player(screen)
                self.board.draw_goal(screen)
                screen.refresh()

        # Recreate path
        path = [cur]
        i, j = cur
        while prevs_s[(i, j)]:
            prev = prevs_s[(i, j)]
            path.append(prev)
            i, j = prev
        path = list(reversed(path))

        i, j = cur
        while prevs_g[(i, j)]:
            prev = prevs_g[(i, j)]
            path.append(prev)
            i, j = prev
        return path


class GreedyBD(Greedy):
    def search(self, start, goal, screen = None):
        '''Performs bidirectional greedy search
        start: (x, y) tuple
        goal: (x, y) tuple
        '''
        costs_s = {}
        prevs_s = {}
        costs_s[start] = 0
        prevs_s[start] = None

        costs_g = {}
        prevs_g = {}
        costs_g[goal] = 0
        prevs_g[goal] = None

        pq_s = PriorityQueue2()
        pq_s.enqueue(start, costs_s[start])

        pq_g = PriorityQueue2()
        pq_g.enqueue(goal, costs_g[goal])

        while not pq_s.isEmpty() and not pq_g.isEmpty():
            cur = pq_s.dequeue()
            cur_x, cur_y = cur

            self.board[cur_y][cur_x] = 3 # Mark as "seen"
            if screen:
                self.board.draw_cell(cur_x, cur_y, screen)

            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                turnCost = self.isTurn(prevs_s[cur], nbr) * 0.2
                cost2nbr = costs_s[cur] + self.getCost(cur, nbr, self.mode_c) + turnCost
                heuristic = self.getHeuristic(nbr, goal, self.mode_h)
                if nbr not in costs_s or cost2nbr < costs_s[nbr]:
                    # Relax costs if cost is lower
                    self.board[nbr[1]][nbr[0]] = 4 # Mark as "frontier"
                    if screen:
                        self.board.draw_cell(nbr[0], nbr[1], screen)

                    # Relax costs
                    costs_s[nbr] = cost2nbr
                    prevs_s[nbr] = cur
                    pq_s.enqueue(nbr,heuristic) # Multiple nodes possible!

            cur = pq_g.dequeue()
            cur_x, cur_y = cur

            self.board[cur_y][cur_x] = 3 # Mark as "seen"
            if screen:
                self.board.draw_cell(cur_x, cur_y, screen)

            if cur in costs_s:
                break

            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                turnCost = self.isTurn(prevs_g[cur], nbr) * 0.2
                cost2nbr = costs_g[cur] + self.getCost(cur, nbr, self.mode_c) + turnCost
                heuristic = self.getHeuristic(nbr, start, self.mode_h)
                if nbr not in costs_g or cost2nbr < costs_g[nbr]: # Relax costs if cost is lower
                    self.board[nbr[1]][nbr[0]] = 4 # Mark as "frontier"
                    if screen:
                        self.board.draw_cell(nbr[0], nbr[1], screen)

                    # Relax costs
                    costs_g[nbr] = cost2nbr
                    prevs_g[nbr] = cur
                    pq_g.enqueue(nbr, heuristic) # Multiple nodes possible!

            if screen:
                self.board.draw_player(screen)
                self.board.draw_goal(screen)
                screen.refresh()

        # Recreate path
        path = [cur]
        i, j = cur
        while prevs_s[(i, j)]:
            prev = prevs_s[(i, j)]
            path.append(prev)
            i, j = prev
        path = list(reversed(path))

        i, j = cur
        while prevs_g[(i, j)]:
            prev = prevs_g[(i, j)]
            path.append(prev)
            i, j = prev
        return path
