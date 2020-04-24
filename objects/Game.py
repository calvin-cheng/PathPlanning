import curses
import time
from objects.PathPlanners import Dijkstra, AStar, Greedy, DijkstraBD, AStarBD, GreedyBD
from objects.Board import Board
from objects.Menu import *


class Game:
    def __init__(self, board, screen):
        self.mode = True # False - Map Edit Mode, True - Simulation

        self.board = board
        self.screen = screen
        self.generate_menus()
        self.menu = 0

        self.initialise_curses()
        self.board.draw(self.screen)
        self.menus[self.menu].display()

        self.player = True
        self.players = {True: self.board.player, False: self.board.goal}
        self.planner = 0
        self.planners = {0: [Dijkstra, DijkstraBD], 
                         1: [AStar, AStarBD], 
                         2: [Greedy, GreedyBD]}

        self.searchActive = False
        self.isRunning = True


    def generate_menus(self):
        menu_sim = Menu(94, 1, 24, 37,
                        [
                         Title('PATHFINDING', 20),
                         Spacer(1),
                         Heading('Algorithm', 20),
                         RadioGroupSingle([
                                           Radio('Dijkstra'),
                                           Radio('A Star'),
                                           Radio('Best First')
                                          ],
                                          20),
                         Heading('Cost', 20),
                         RadioGroupSingle([
                                           Radio('Manhattan'),
                                           Radio('Euclidean')
                                          ],
                                          20),
                         Heading('Heuristic', 20),
                         RadioGroupSingle([
                                           Radio('Manhattan'),
                                           Radio('Euclidean')
                                          ],
                                          20),
                         Heading('Options', 20),
                         RadioGroupMultiple([
                                             Radio('Bidirectional'),
                                            ],
                                            20),
                         Button('Pathfind', self.search, 20, 3),
                         Button('Edit Board', self.switch_menu, 20, 3),
                         ButtonGroup([
                                      Button('Clear', self.clear, 13, 3),
                                      Button('Quit', self.quit, 6, 3)
                                     ], 20)
                        ],
                        self.screen)
        menu_edit = Menu(94, 1, 24, 37,
                         [
                          Button('Move Start', self.move_player, 20, 3),
                          Button('Move Goal', self.move_goal, 20, 3),
                          Button('Mazify', self.mazify, 20, 3),
                          Button('Reset', self.board.generate, 20, 3),
                          Button('Done', self.switch_menu, 20, 3)
                         ],
                         self.screen)
        menus = [menu_sim, menu_edit]
        self.menus = menus

    def move_player(self):
        self.player = True
        self.switch_mode()

    def move_goal(self):
        self.player = False
        self.switch_mode()


    def initialise_curses(self):
        self.screen.clear()
        curses.curs_set(0)
        curses.use_default_colors()

        # (i, fg, bg), 0 reserved. fg, bg = -1 for default values
        curses.init_pair(1, curses.COLOR_WHITE, -1)  # Gap
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)    # Player
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN) # Goal
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW) # Path
        curses.init_pair(5, curses.COLOR_WHITE, -1) # Visited
        curses.init_pair(6, curses.COLOR_CYAN, -1) # Frontier

    def start(self):
        while self.isRunning:
            key = self.screen.getch()
            if self.mode == True: 
                # Simulation
                if key == curses.KEY_UP:
                    self.menus[self.menu].nav(-1)
                elif key == curses.KEY_DOWN:
                    self.menus[self.menu].nav(1)
                elif key == curses.KEY_RIGHT:
                    self.menus[self.menu].navX(1)
                elif key == curses.KEY_LEFT:
                    self.menus[self.menu].navX(-1)
                elif key == ord(' '):
                    self.menus[self.menu].select()
            else: 
                # Map-edit
                # Update player or goal position
                self.players = {True: self.board.player, False: self.board.goal}
                if key == curses.KEY_UP:
                    self.board.moveNode(self.players[self.player], 'U')
                elif key == curses.KEY_DOWN:
                    self.board.moveNode(self.players[self.player], 'D')
                elif key == curses.KEY_RIGHT:
                    self.board.moveNode(self.players[self.player], 'R')
                elif key == curses.KEY_LEFT:
                    self.board.moveNode(self.players[self.player], 'L')
                elif key == ord(' '):
                    self.switch_mode()
                if self.searchActive:
                    self.search(False)

            self.board.draw(self.screen)
            self.menus[self.menu].display()

    def search(self, animate = True):
        self.board.clearPath()
        self.board.draw(self.screen)

        # Set pathfinding parameters
        mode_c = self.menus[0].items[5].state
        mode_h = self.menus[0].items[7].state
        planner = self.menus[0].items[3].state
        bd = self.menus[0].items[9].radios[0].state

        # Create pathfinder object
        pathfinder = self.planners[planner][bd](self.board, mode_c, mode_h)
        if animate:
            path = pathfinder.search(self.board.player, self.board.goal, self.screen)
        else:
            path = pathfinder.search(self.board.player, self.board.goal)

        # Draw path
        for node in path:
            i, j = node
            self.board[j][i] = 2
            self.board.draw_cell(i, j, self.screen)
            self.board.draw_player(self.screen)
            self.board.draw_goal(self.screen)
            if animate:
                self.screen.refresh()
                time.sleep(0.03)

        curses.flushinp() # Clears key inputs from queue
        self.searchActive = True

    def switch_player(self):
        self.player = not(self.player)

    def switch_planner(self, n):
        self.planner = n

    def switch_menu(self):
        self.menu = (self.menu + 1) % 2
        self.menus[self.menu].show()

    def switch_mode(self):
        self.mode = not(self.mode)

    def mazify(self):
        self.searchActive = False
        self.board.mazify()

    def clear(self):
        self.searchActive = False
        self.board.clearPath()

    def quit(self):
        self.isRunning = False

