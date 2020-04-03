import curses
import time
import random
# from objects.Linear import PriorityQueue
from objects.PathPlanners import Djikstra

# Maze Generation Testing
class Maze:
    def __init__(self, length, width):
        '''Constructor'''
        # Maze composed of 2x2 cells
        self.l = (length*2-1) + 2
        self.w = (width*2-1) + 2
        self.board, self.playerPos, self.goal = self.generate() 

    def __str__(self):
        '''Allows Maze object to be printed via print()'''
        string = ''
        for y in range(self.l):
            for x in range(self.w):
                if self.playerPos == [x, y]:
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
        h, w = stdscr.getmaxyx()

        # Draw walls
        # Double horizontal spacing for better aspect ratio
        for i in range(self.w):
            for j in range(self.l):
                if self.board[j][i] == 1: # Wall
                    #char = u'\u25a0'
                    char = '  '
                    colorIdx = 2
                elif self.board[j][i] == 2: # Path
                    char = '  '
                    colorIdx = 4
                else: # self.board[j][i] == 0 # Gap
                    char = '  '
                    colorIdx = 1
                stdscr.attron(curses.color_pair(colorIdx))
                stdscr.addstr(h//2 - self.l//2 + j, w//2 - self.w + i*2, char)
                stdscr.attroff(curses.color_pair(colorIdx))

        # Draw player
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(h//2 - self.l//2 + self.playerPos[0],
                     w//2 - self.w + self.playerPos[1]*2,
                     '  ')
        stdscr.attroff(curses.color_pair(3))
        stdscr.refresh()
        
    def generate(self):
        '''Generates random maze using DFS and moves player to start'''
        self.board = [[1 for _ in range(self.w)] for _ in range(self.l)]
        X, Y = random.randrange(1,self.w - 1,2), random.randrange(1,self.l - 1,2)
        self.board[Y][X] = 0
        self.carve(X,Y)

        # Set start and valid positions, move player to start
        startX, endX = 1, self.w-2
        self.board[0][startX] = 0
        self.board[-1][endX] = 0
        self.playerPos = [0, startX]
        self.goal = [self.l-1, endX]

        return self.board, self.playerPos, self.goal

    def carve(self, X, Y):
        '''Helper recursive function for DFS maze generation.
        "Carves" a tunnel from position (X, Y).
        '''
        DIRS = [[0, -2], [2, 0], [0, 2], [-2, 0]] # N, E, S, W
        random.shuffle(DIRS)
        for dX, dY in DIRS:
            if self.inBoard(X+dX,Y+dY) and self.board[Y+dY][X+dX] == 1:
                for x in range(min(X, X+dX), max(X, X+dX)+1):
                    for y in range(min(Y, Y+dY), max(Y, Y+dY)+1):
                        self.board[y][x] = 0
                self.carve(X+dX, Y+dY)

    def inBoard(self, x, y):
        '''Helper function that returns TRUE if (x,y) is valid.'''
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
        res = []
        for dx, dy in dirs:
            if self.inBoard(x + dx, y + dy) and self.board[y+dy][x+dx] != 1:
                res.append((x + dx, y + dy))
        return res

    def __getitem__(self, i):
        return self.board[i]

    def __len__(self):
        return len(self.board)

    def movePlayer(self, direction):
        '''Moves player if valid'''
        dirs = {'U': [-1, 0], 'D': [1, 0], 'L': [0, -1], 'R': [0, 1]}
#         wallCheck = {'U': [-1, 0], 'D': [1, 0], 'L': [0, -1], 'R': [0, 1]}
        dY, dX = dirs[direction]
#         wY, wX = wallCheck[direction]
        pY, pX = self.playerPos
        if self.inBoard(pX+dX, pY+dY) and self.board[pY+dY][pX+dX] != 1:
            self.playerPos = [pY+dY, pX+dX]

    def checkWin(self):
        return self.playerPos == self.goal

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)

    # (i, fg, bg), i >= 1 for some reason
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)  # Gap
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)  # Wall 
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED)    # Player
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW) # Path

    h, w = stdscr.getmaxyx()
    m = Maze(h//3, w//6)
    
    m.draw(stdscr)
    string = "(S)earch   |   (Q)uit"
    stdscr.addstr(h//2 + m.l//2 + 3, w//2 - len(string)//2, string)

    while True:
        h, w = stdscr.getmaxyx()
        key = stdscr.getch()
        if key == curses.KEY_UP:
            m.movePlayer('U')
            m.draw(stdscr)
        elif key == curses.KEY_DOWN:
            m.movePlayer('D')
            m.draw(stdscr)
        elif key == curses.KEY_RIGHT:
            m.movePlayer('R')
            m.draw(stdscr)
        elif key == curses.KEY_LEFT:
            m.movePlayer('L')
            m.draw(stdscr)
        elif key == ord('q'):
            curses.curs_set(1)
            break
        elif key == ord('s'):
            d = Djikstra(m)
            # TODO: fix naming conventions (playerPos in [Y, X], nodes in (X, Y))
            path = d.search((m.playerPos[1],m.playerPos[0]), (m.goal[1],m.goal[0]))
            for node in path:
                i, j = node
                time.sleep(0.04)
                m.board[j][i] = 2
                m.draw(stdscr)

        if m.checkWin():
            stdscr.clear()
            string = "You win, noice!"
            stdscr.addstr(h//2, w//2 - len(string)//2, string)
            stdscr.refresh()
            time.sleep(1.5)
            break

curses.wrapper(main)



