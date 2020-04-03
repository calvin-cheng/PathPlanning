import curses
import time
import random

# Maze Generation Testing
class Maze:
    def __init__(self, length, width):
        '''Constructor'''
        # Maze composed of 2x2 cells
        self.l = (length*2-1) + 2
        self.w = (width*2-1) + 2
        self.generate()    # Creates board, playerPos and goal properties


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
       # stdscr.clear()
        h, w = stdscr.getmaxyx()
        for i in range(self.w):
            for j in range(self.l):
                # char = u'\u25a0' if self.board[j][i] else ' '
                stdscr.attron(curses.color_pair(self.board[j][i] + 1))
                stdscr.addch(h//2 - self.l//2 + j, 
                             w//2 - self.w//2 + i, 
                             ' ')
                stdscr.attroff(curses.color_pair(self.board[j][i] + 1))

        stdscr.addch(h//2 - self.l//2 + self.playerPos[0],
                     w//2 - self.w//2 + self.playerPos[1],
                     '*')
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
        if x < 0 or x >= self.w or y < 0 or y >= self.l:
            result = False
        else:
            result = True
        return result

    def movePlayer(self, direction):
        '''Moves player if valid'''
        dirs = {'U': [-1, 0], 'D': [1, 0], 'L': [0, -2], 'R': [0, 2]}
        wallCheck = {'U': [-1, 0], 'D': [1, 0], 'L': [0, -1], 'R': [0, 1]}
        dY, dX = dirs[direction]
        wY, wX = wallCheck[direction]
        pY, pX = self.playerPos
        if self.inBoard(pX+dX, pY+dY) and not self.board[pY+wY][pX+wX]:
            self.playerPos = [pY+dY, pX+dX]

    def checkWin(self):
        return self.playerPos == self.goal

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)

    # (i, fg, bg), i >= 1 for some reason
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) # Gap
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE) # Wall 

    h, w = stdscr.getmaxyx()
    m = Maze(h//4, w//4)
    
    m.draw(stdscr)
    string = "(Q)uit"
    stdscr.addstr(h//2 + m.l//2 + 3, w//2 - len(string)//2, string)

    while True:
        h, w = stdscr.getmaxyx()
        key = stdscr.getch()
        if key == curses.KEY_UP:
            m.movePlayer('U')
            m.draw(stdscr)
            string = "(Q)uit"
            stdscr.addstr(h//2 + m.l//2 + 3, w//2 - len(string)//2, string)
        elif key == curses.KEY_DOWN:
            m.movePlayer('D')
            m.draw(stdscr)
            string = "(Q)uit"
            stdscr.addstr(h//2 + m.l//2 + 3, w//2 - len(string)//2, string)
        elif key == curses.KEY_RIGHT:
            m.movePlayer('R')
            m.draw(stdscr)
            string = "(Q)uit"
            stdscr.addstr(h//2 + m.l//2 + 3, w//2 - len(string)//2, string)
        elif key == curses.KEY_LEFT:
            m.movePlayer('L')
            m.draw(stdscr)
            string = "(Q)uit"
            stdscr.addstr(h//2 + m.l//2 + 3, w//2 - len(string)//2, string)
        elif key == ord('q'):
            curses.curs_set(1)
            break
        if m.checkWin():
            stdscr.clear()
            string = "You win, noice!"
            stdscr.addstr(h//2, w//2 - len(string)//2, string)
            stdscr.refresh()
            time.sleep(1.5)
            break

curses.wrapper(main)



