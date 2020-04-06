# Maze Generation Testing
class Board:
    def __init__(self, length, width):
        '''Constructor'''
        # Board composed of 2x2 cells
        self.l = (length * 2 - 1) + 2
        self.w = (width * 2 - 1) + 2
        self.board = [[0 for _ in range(self.w)] for _ in range(self.l)]
        self.player = (1, 1)
        self.goal = (self.w - 2, self.l - 2)
        self.generate()

    def __str__(self):
        '''Allows Maze object to be printed via print()'''
        string = ''
        for y in range(self.l):
            for x in range(self.w):
                if self.player == [x, y]:
                    string += '•'
                else:
                    if self.board[y][x] == 1:
                        string += '#'
                    else:
                        string += ' '
            string += '\n'
        return string

    def draw(self, stdscr):
        '''Draws maze and player on curses screen object'''
        import curses
        h, w = stdscr.getmaxyx()

        # Draw walls
        # Double horizontal spacing for better aspect ratio
        for i in range(self.w):
            for j in range(self.l):
                if self.board[j][i] == 1: # Wall
                    string = '  '
                    attr = curses.color_pair(1) | curses.A_BOLD | curses.A_STANDOUT
                elif self.board[j][i] == 2: # Path
                    string = '  '
                    attr = curses.color_pair(4)
                elif self.board[j][i] == 0: # Gap
                    string = '  '
                    attr = curses.color_pair(1)

                stdscr.addstr(h//2 - self.l//2 + j - 2, w//2 - self.w + i*2, string, attr)

        # Draw player
        stdscr.addstr(h//2 - self.l//2 - 2 + self.player[1],
                      w//2 - self.w + self.player[0]*2,
                      '  ', curses.color_pair(2))
        # Draw goal
        stdscr.addstr(h//2 - self.l//2 - 2 + self.goal[1],
                      w//2 - self.w + self.goal[0]*2,
                      '  ', curses.color_pair(3) | curses.A_BOLD)
        stdscr.refresh()
        
    def generate(self):
        '''Generates an empty board with border walls'''
        self.board = [[1 for _ in range(self.w)] for _ in range(self.l)]
        for i in range(1, self.w-1):
            for j in range(1, self.l-1):
                self.board[j][i] = 0

    def mazify(self):
        '''Generates random maze using DFS and moves player to start'''
        import random
        self.board = [[1 for _ in range(self.w)] for _ in range(self.l)]
        X, Y = random.randrange(1,self.w - 1,2), random.randrange(1,self.l - 1,2)
        self.board[Y][X] = 0
        self.carve(X,Y)

        # Set start and valid positions, move player to start
        startX, endX = 1, self.w-2
        self.board[0][startX] = 0
        self.board[-1][endX] = 0
        self.player = (startX, 0)
        self.goal = (endX, self.l - 1)

    def carve(self, X, Y):
        '''Helper recursive function for DFS maze generation.
        "Carves" a tunnel from position (X, Y).
        '''
        import random
        DIRS = [[0, -2], [2, 0], [0, 2], [-2, 0]] # N, E, S, W
        random.shuffle(DIRS)
        for dX, dY in DIRS:
            if self.inBoard(X+dX,Y+dY) and self.board[Y+dY][X+dX] == 1:
                for x in range(min(X, X+dX), max(X, X+dX)+1):
                    for y in range(min(Y, Y+dY), max(Y, Y+dY)+1):
                        self.board[y][x] = 0
                self.carve(X+dX, Y+dY)

    def clearPath(self):
        '''Removes path nodes from board'''
        for i in range(self.w):
            for j in range(self.l):
                if self.board[j][i] == 2:
                    self.board[j][i] = 0

    def inBoard(self, x, y):
        '''Helper function that returns TRUE if (x, y) is valid.'''
        if (x >= 0 and x < self.w) and (y >= 0 and y < self.l):
            result = True
        else:
            result = False
        return result

    def getNeighbours(self, node):
        '''Gets neighbours of node
        node: (x, y) tuple
        '''
        x, y = node
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbours = []
        for dx, dy in dirs:
            if self.inBoard(x + dx, y + dy) and self.board[y+dy][x+dx] != 1:
                neighbours.append((x + dx, y + dy))
        return neighbours

    def __getitem__(self, i):
        return self.board[i]

    def __len__(self):
        return len(self.board)

    def movePlayer(self, direction):
        '''Moves player if valid'''
        dirs = {'U': [-1, 0], 'D': [1, 0], 'L': [0, -1], 'R': [0, 1]}
        dY, dX = dirs[direction]
        pX, pY = self.player
        if self.inBoard(pX+dX, pY+dY) and self.board[pY+dY][pX+dX] != 1:
            self.player = (pX+dX, pY+dY)

    def checkWin(self):
        return self.player == self.goal


