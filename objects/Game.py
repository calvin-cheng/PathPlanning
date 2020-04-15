import curses
import time
from objects.PathPlanners import Dijkstra, AStar
from objects.Board import Board
from objects.Menu import Menu, Radio, Button


class Game:
    def __init__(self, board, screen):

        self.mode = True # False - Map Edit Mode, True - Simulation

        self.board = board
        self.screen = screen
        self.generate_menu()

        self.initialise_curses()
        self.draw_board()
        self.draw_menu()

        self.player = True
        self.players = {True: self.board.player, False: self.board.goal}
        self.planner = 0
        self.planners = {0: Dijkstra, 1: AStar}
        self.isRunning = True


    def generate_menu(self):
        self.menu = Menu(94, 1, 
                         [
                          Radio('Toggle Me'),
                          Button('Edit Board', self.switch_mode),
                          Button('Pathfind!', self.search),
                          Button('Clear', self.board.clearPath),
                          Button('Quit', self.quit)
                         ],
                         self.screen)

    def initialise_curses(self):
        self.screen.clear()
        curses.curs_set(0)
        curses.use_default_colors()

        # (i, fg, bg), 0 reserved. fg, bg = -1 for default values
        curses.init_pair(1, -1, -1)  # Gap
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)    # Player
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN) # Goal
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW) # Path
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE) # Visited
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_CYAN) # Frontier

    def start(self):
        while self.isRunning:
            key = self.screen.getch()
            if self.mode == True: 
                # Simulation
                if key == curses.KEY_UP:
                    self.menu.nav(-1)
                elif key == curses.KEY_DOWN:
                    self.menu.nav(1)
                elif key == ord(' '):
                    self.menu.select()
                elif key == ord('p'):
                    self.switch_planner()
            else: 
                # Map-edit
                # TODO: Fix below
                self.players = {True: self.board.player, False: self.board.goal}
                if key == curses.KEY_UP:
                    self.board.moveNode(self.players[self.player], 'U')
                elif key == curses.KEY_DOWN:
                    self.board.moveNode(self.players[self.player], 'D')
                elif key == curses.KEY_RIGHT:
                    self.board.moveNode(self.players[self.player], 'R')
                elif key == curses.KEY_LEFT:
                    self.board.moveNode(self.players[self.player], 'L')
                elif key == ord('q'):
                    self.switch_mode()
                elif key == ord('m'):
                    self.board.mazify()
                elif key == ord('r'):
                    self.board.generate()
                elif key == ord('t'):
                    self.switch_player()
            self.draw_board()
            self.draw_menu()

    def draw_menu(self):
        y, x = self.menu.window.getmaxyx()
        title = 'PATH-FINDER'
        self.menu.window.addstr(1, x//2 - len(title)//2, title, 
                curses.A_BOLD | curses.A_UNDERLINE)
        for idx, item in enumerate(self.menu.items):
            if self.mode and self.menu.pos == idx:
                attr = curses.A_BOLD | curses.A_REVERSE
            else:
                attr = curses.A_BOLD
            self.menu.window.addstr(3+idx, 2, item.string(), attr)
        self.menu.window.addstr(3+idx+1, 2, '') # Prevent underline hiding
        self.menu.window.box()
        self.menu.window.refresh()

    def draw_board(self):
        '''Draws board and player on curses screen object'''
        h, w = self.screen.getmaxyx()

        # Draw walls
        # Double horizontal spacing for better aspect ratio
        for i in range(self.board.w):
            for j in range(self.board.l):
                if self.board[j][i] == 0: # Gap
                    string = '  '
                    attr = curses.color_pair(1)
                elif self.board[j][i] == 1: # Wall
                    string = '  '
                    attr = curses.color_pair(1) | curses.A_BOLD | curses.A_STANDOUT
                elif self.board[j][i] == 2: # Path
                    string = '  '
                    attr = curses.color_pair(4)
                elif self.board[j][i] == 3: # Visited
                    string = '  '
                    attr = curses.color_pair(5)
                elif self.board[j][i] == 4: # Marked
                    string = '  '
                    attr = curses.color_pair(6) | curses.A_STANDOUT

                self.screen.addstr(1 + j, 2 + i * 2, string, attr)

        # Draw player
        self.screen.addstr(1 + self.board.player[1],
                           2 + self.board.player[0]*2,
                           '  ', curses.color_pair(2))
        # Draw goal
        self.screen.addstr(1 + self.board.goal[1],
                           2 + self.board.goal[0]*2,
                           '  ', curses.color_pair(3) | curses.A_BOLD)
        self.screen.refresh()

    def switch_player(self):
        self.player = not(self.player)

    def switch_mode(self):
        self.mode = not(self.mode)

    def switch_planner(self):
        planner = (planner + 1) % 2

    def quit(self):
        self.isRunning = False

    def search(self):
        self.board.clearPath()
        d = self.planners[self.planner](self.board)
        path = d.search(self.board.player, self.board.goal, self.screen)
        for node in path:
            i, j = node
            time.sleep(0.04)
            self.board[j][i] = 2
            self.draw_board()
            curses.flushinp() # Clears key inputs from queue



