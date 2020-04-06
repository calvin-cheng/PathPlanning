class Djikstra:
    def __init__(self, board):
        self.board = board

    def search(self, start, goal):
        '''Performs search using Djikstra's algorithm
        start: (x, y) tuple
        goal: (x, y) tuple
        '''

        dists = [[9999] * len(self.board[0]) for _ in range(len(self.board))]
        prevs = [[None] * len(self.board[0]) for _ in range(len(self.board))]
        startX, startY = start
        dists[startY][startX] = 0

        from objects.LinearADT import PriorityQueue
        pq = PriorityQueue([], [])
        for i in range(len(self.board[0])):
            for j in range(len(self.board)):
                if self.board[j][i] == 1:
                    continue
                node = (i, j)
                dist = dists[j][i]
                pq.enqueue(node, dist)

        while not pq.isEmpty():
            cur = pq.dequeue()
            cur_x, cur_y = cur
            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                nbr_x, nbr_y = nbr
                dist2nbr = dists[cur_y][cur_x] + self.getDist(cur, nbr)
                if dists[nbr_y][nbr_x] > dist2nbr:
                    dists[nbr_y][nbr_x] = dist2nbr
                    prevs[nbr_y][nbr_x] = cur
                    pq.setPriority(nbr, dist2nbr)

        # Recreate path
        path = [goal]
        i, j = goal
        while prevs[j][i]:
            prev = prevs[j][i]
            path.append(prev)
            i, j = prev

        return path[::-1]

    def getDist(self, node1, node2):
        '''Finds manhattan distance between node1 and node2
        node1: (x, y) tuple
        node2: (x, y) tuple
        '''
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])


class AStar:
    def __init__(self, board):
        self.board = board

    def search(self, start, goal):
        '''Performs search using AStar algorithm
        start: (x, y) tuple
        goal: (x, y) tuple
        '''

        dists = [[9999] * len(self.board[0]) for _ in range(len(self.board))]
        prevs = [[None] * len(self.board[0]) for _ in range(len(self.board))]
        startX, startY = start
        dists[startY][startX] = 0

        from objects.LinearADT import PriorityQueue
        pq = PriorityQueue([], [])
        for i in range(len(self.board[0])):
            for j in range(len(self.board)):
                if self.board[j][i] == 1:
                    continue
                node = (i, j)
                dist = dists[j][i]
                pq.enqueue(node, dist)

        while not pq.isEmpty():
            cur = pq.dequeue()
            cur_x, cur_y = cur
            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                nbr_x, nbr_y = nbr
                dist2nbr = (dists[cur_y][cur_x] 
                            + self.getDist(cur, nbr) # Cost
                            - self.getDist(nbr, goal)) # Heuristic
                if dists[nbr_y][nbr_x] > dist2nbr:
                    dists[nbr_y][nbr_x] = dist2nbr
                    prevs[nbr_y][nbr_x] = cur
                    pq.setPriority(nbr, dist2nbr)

        # Recreate path
        path = [goal]
        i, j = goal
        while prevs[j][i]:
            prev = prevs[j][i]
            path.append(prev)
            i, j = prev

        return path[::-1]

    def getDist(self, node1, node2):
        '''Finds manhattan distance between node1 and node2
        node1: (x, y) tuple
        node2: (x, y) tuple
        '''
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

