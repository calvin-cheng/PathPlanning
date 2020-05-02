# Maze Generation Testing
import curses
import random


class Board:
    def __init__(self, length, width):
        '''Constructor'''
        # Board composed of 2x2 cells
        self.l = (length * 2 - 1) + 2
        self.w = (width * 2 - 1) + 2
        self.board = [[0 for _ in range(self.w)] for _ in range(self.l)]
        self.start = (3, self.l//2)
        self.goal = (self.w - 4, self.l//2)
        self.cursor = (1, 1)
        self.generate()

    def __str__(self):
        '''Allows Maze object to be printed via print()'''
        string = ''
        for y in range(self.l):
            for x in range(self.w):
                if self.start == [x, y]:
                    string += '•'
                else:
                    if self.board[y][x] == 1:
                        string += '#'
                    else:
                        string += ' '
            string += '\n'
        return string

        
    def draw(self, screen):
        '''Draws board and start/goal on curses screen object'''
        h, w = screen.getmaxyx()

        # Draw walls
        # Double horizontal spacing for better aspect ratio
        for i in range(self.w):
            for j in range(self.l):
                if self.board[j][i] == 0: # Gap
                    string = '  '
                    attr = curses.color_pair(1)
                elif self.board[j][i] == 1: # Wall
                    string = '  '
                    attr = curses.color_pair(1) | curses.A_BOLD | curses.A_STANDOUT
                elif self.board[j][i] == 2: # Path
                    string = u'\u2805\u2805'
                    attr = curses.color_pair(4) | curses.A_BOLD
                elif self.board[j][i] == 3: # Visited
                    string = u'\u2805'*2 
                    attr = curses.color_pair(5) | curses.A_BOLD
                elif self.board[j][i] == 4: # Frontier
                    string = u'\u2805'*2 
                    attr = curses.color_pair(6) | curses.A_BOLD #| curses.A_STANDOUT

                screen.addstr(1 + j, 2 + i * 2, string, attr)

        self.draw_start(screen)
        self.draw_goal(screen)

    def draw_cell(self, i, j, screen):
        if self.board[j][i] == 0: # Gap
            string = '  '
            attr = curses.color_pair(1)
        elif self.board[j][i] == 1: # Wall
            string = '  '
            attr = curses.color_pair(1) | curses.A_BOLD | curses.A_STANDOUT
        elif self.board[j][i] == 2: # Path
            string = u'\u2805\u2805'
            attr = curses.color_pair(4) | curses.A_BOLD
        elif self.board[j][i] == 3: # Visited
            string = u'\u2805'*2 
            attr = curses.color_pair(5) | curses.A_BOLD
        elif self.board[j][i] == 4: # Frontier
            string = u'\u2805'*2 
            attr = curses.color_pair(6) | curses.A_BOLD #| curses.A_STANDOUT

        screen.addstr(1 + j, 2 + i * 2, string, attr)

    def draw_start(self, screen):
        screen.addstr(1 + self.start[1],
                      2 + self.start[0]*2,
                      '  ', curses.color_pair(2))

    def draw_goal(self, screen):
        screen.addstr(1 + self.goal[1],
                      2 + self.goal[0]*2,
                      '  ', curses.color_pair(3) | curses.A_BOLD)

    def draw_cursor(self, screen):
        i, j = self.cursor
        if self.cursor == self.start:
            attr = curses.color_pair(2)
        elif self.cursor == self.goal:
            attr = curses.color_pair(3) | curses.A_BOLD
        elif self.board[j][i] == 1:
            attr = curses.color_pair(1) | curses.A_BOLD | curses.A_STANDOUT
        else:
            attr = curses.color_pair(0)

        screen.addstr(1 + self.cursor[1],
                      2 + self.cursor[0]*2,
                      u'\u283f\u283f', attr)

    def clearPath(self):
        '''Removes path nodes from board'''
        for i in range(self.w):
            for j in range(self.l):
                if self.board[j][i] != 1:
                    self.board[j][i] = 0

    def generate(self):
        '''Generates an empty board with border walls'''
        self.board = [[1 for _ in range(self.w)] for _ in range(self.l)]
        for i in range(1, self.w-1):
            for j in range(1, self.l-1):
                self.board[j][i] = 0

    def mazify(self):
        '''Generates random maze using DFS and moves player to start'''
        self.board = [[1 for _ in range(self.w)] for _ in range(self.l)]
        x, y = random.randrange(1,self.w - 1,2), random.randrange(1,self.l - 1,2)
        self.board[y][x] = 0
        self.carve(x, y)

        # Delete walls directly above start and goal
        start_x, start_y = self.start
        goal_x, goal_y = self.goal
        self.board[start_y][start_x] = 0
        self.board[goal_y][goal_x] = 0

    def carve(self, x, y):
        '''Helper recursive function for DFS maze generation.
        "Carves" a tunnel from position (x, y).
        '''
        DIRS = [(0, -2), (2, 0), (0, 2), (-2, 0)] # N, E, S, W
        random.shuffle(DIRS)
        for dx, dy in DIRS:
            if self.inBoard(x+dx,y+dy) and self.board[y+dy][x+dx] == 1:
                # Open wall between (x, y) and (x+dx, y+dy)
                for i in range(min(y, y+dy), max(x, x+dx)+1):
                    for j in range(min(y, y+dy), max(y, y+dy)+1):
                        self.board[j][i] = 0
                self.carve(x+dx, y+dy)

    def inBoard(self, x, y):
        '''Helper function that returns TRUE if (x, y) is valid.'''
        return (0 <= x < self.w) and (0 <= y < self.l)

    def getNeighbours(self, node):
        '''Gets neighbouring free nodes within the board
        node: (x, y) tuple
        '''
        x, y = node
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        nbrs = []
        for dx, dy in dirs:
            if self.inBoard(x+dx, y+dy) and self.board[y+dy][x+dx] != 1:
                nbrs.append((x+dx, y+dy))
        return nbrs

    def __getitem__(self, i):
        return self.board[i]

    def __len__(self):
        return len(self.board)

    def placeStart(self, pos):
        '''Places start at pos = (x, y)'''
        new_x, new_y = pos
        if self.inBoard(new_x, new_y):
            self.start = (new_x, new_y)
            self.board[new_y][new_x] = 0

    def moveStart(self, direction):
        '''Moves start node'''
        dirs = {'U': [-1, 0], 'D': [1, 0], 'L': [0, -1], 'R': [0, 1]}
        dy, dx = dirs[direction]
        x, y = self.start
        if self.board[y+dy][x+dx] != 1:
            self.placeStart((x+dx, y+dy))

    def placeGoal(self, pos):
        '''Places goal at pos = (x, y)'''
        new_x, new_y = pos
        if self.inBoard(new_x, new_y):
            self.goal = (new_x, new_y)
            self.board[new_y][new_x] = 0

    def moveGoal(self, direction):
        '''Moves goal node'''
        dirs = {'U': [-1, 0], 'D': [1, 0], 'L': [0, -1], 'R': [0, 1]}
        dy, dx = dirs[direction]
        x, y = self.goal
        if self.board[y+dy][x+dx] != 1:
            self.placeGoal((x+dx, y+dy))

    def moveCursor(self, direction):
        '''Moves cursor'''
        dirs = {'U': [-1, 0], 'D': [1, 0], 'L': [0, -1], 'R': [0, 1]}
        dy, dx = dirs[direction]
        x, y = self.cursor
        if self.inBoard(x+dx, y+dy):
            self.cursor = (x+dx, y+dy)
