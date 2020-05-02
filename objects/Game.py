import curses
import time
from objects.PathPlanners import Dijkstra, AStar, Greedy, DijkstraBD, AStarBD, GreedyBD
from objects.Board import Board
from objects.Menu import *


class Game:
    def __init__(self, board, screen):
        self.mode = 0 # 0 - Simulation, 1 - Board Edit

        self.board = board
        self.screen = screen
        self.generate_menus()
        self.menu = 0 # 0 - Simulation, 1 - Board Edit, 2 - Editing Instructions

        self.initialise_curses()
        self.board.draw(self.screen)
        self.menus[self.menu].display()

        self.player = 0
        self.players = {0: self.board.start, 
                        1: self.board.goal, 
                        2: self.board.cursor}
        self.planner = 0
        self.planners = {0: [Dijkstra, DijkstraBD], 
                         1: [AStar, AStarBD], 
                         2: [Greedy, GreedyBD]}
        self.cursorMode = 0

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
                         Button('Edit Board', lambda: self.switch_menu(1), 20, 3),
                         ButtonGroup([
                                      Button('Clear', self.clear, 13, 3),
                                      Button('Quit', self.quit, 6, 3)
                                     ], 20)
                        ],
                        self.screen)
        menu_edit = Menu(94, 1, 24, 37,
                         [
                          Title('Board Edit', 20),
                          Spacer(1),
                          Heading('Basic', 20),
                          Spacer(1),
                          Button('Move Start', lambda: self.set_player(0), 20, 3),
                          Button('Move Goal', lambda: self.set_player(1), 20, 3),
                          Button('Reset', self.board.generate, 20, 3),
                          Spacer(1),
                          Heading('Advanced', 20),
                          Spacer(1),
                          Button('Add/Remove Walls', lambda: self.set_player(2), 20, 3),
                          Button('Mazify', self.mazify, 20, 3),
                          Spacer(10),
                          Button('Done', lambda: self.switch_menu(0), 20, 3)
                         ],
                         self.screen)
        menu_startgoal = Menu(94, 1, 24, 37,
                              [
                               Spacer(12),
                               Heading('Controls', 20),
                               Spacer(1),
                               Text('ARROW KEYS: Move', 20),
                               Text('Q: Finish', 20),
                              ],
                              self.screen)
        menu_cursor = Menu(94, 1, 24, 37,
                              [
                               Spacer(12),
                               Heading('Controls', 20),
                               Spacer(1),
                               Text('ARROW KEYS: Move', 20),
                               Text('1: Place Start', 20),
                               Text('2: Place Goal', 20),
                               Text('SPACE: Add Walls', 20),
                               Text('Q: Finish', 20),
                              ],
                              self.screen)
                          
        menus = [menu_sim, menu_edit, menu_startgoal, menu_cursor]
        self.menus = menus



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
            if self.mode == 0: 
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

            elif self.mode == 1: 
                # Map-edit
                # Update player or goal position
                self.players = {0: self.board.start, 1: self.board.goal, 2: self.board.cursor}
                if key == curses.KEY_UP:
                    self.move_player('U')
                elif key == curses.KEY_DOWN:
                    self.move_player('D')
                elif key == curses.KEY_RIGHT:
                    self.move_player('R')
                elif key == curses.KEY_LEFT:
                    self.move_player('L')
                elif key == ord('q'):
                    self.switch_mode(0)
                    self.switch_menu(1)

                if self.searchActive:
                    self.search(False)

            elif self.mode == 2:
                # Cursor
                if key == curses.KEY_UP:
                    self.move_player('U')
                elif key == curses.KEY_DOWN:
                    self.move_player('D')
                elif key == curses.KEY_RIGHT:
                    self.move_player('R')
                elif key == curses.KEY_LEFT:
                    self.move_player('L')
                elif key == ord('q'):
                    self.switch_mode(0)
                    self.switch_menu(1)
                elif key == ord('1'):
                    self.board.placePlayer(self.board.cursor)
                elif key == ord('2'):
                    self.board.placeGoal(self.board.cursor)
                elif key == ord(' '):
                    self.switch_cursor_mode()

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
            path = pathfinder.search(self.board.start, self.board.goal, self.screen)
        else:
            path = pathfinder.search(self.board.start, self.board.goal)

        # Draw path if found
        if path:
            for node in path:
                i, j = node
                self.board[j][i] = 2
                self.board.draw_cell(i, j, self.screen)
                self.board.draw_start(self.screen)
                self.board.draw_goal(self.screen)
                if animate:
                    self.screen.refresh()
                    time.sleep(0.02)

        curses.flushinp() # Clears key inputs from queue
        self.searchActive = True

    def set_player(self, n):
        self.player = n
        if self.player == 0 or self.player == 1:
            self.switch_mode(1)
            self.switch_menu(2)
        elif self.player == 2:
            self.switch_mode(2)
            self.switch_menu(3)


    def move_player(self, direction):
        ''' Moves "player" (ie. start, goal, cursor) '''
        if self.player == 0:
            self.board.moveStart(direction)
        elif self.player == 1:
            self.board.moveGoal(direction)
        else:
            self.board.moveCursor(direction)
            x, y = self.board.cursor
            if self.cursorMode == 1: # Adding walls
                self.board[y][x] = 1
            elif self.cursorMode == 2: # Removing walls
                self.board[y][x] = 0

    def switch_cursor_mode(self):
        '''Switches cursor mode
        0 - Neutral, 1 - Adds walls, 2 - Removes walls
        '''
        if self.cursorMode != 0:
            self.cursorMode = 0

        else:
            x, y = self.board.cursor
            if self.board[y][x] == 1:
                self.board[y][x] = 0
                self.cursorMode = 2
            else:
                self.board[y][x] = 1
                self.cursorMode = 1

    def switch_menu(self, n):
        '''Switches menu'''
        self.menu = n
        self.menus[self.menu].show()

    def switch_mode(self, n):
        '''Switches game mode
        n: 0 - Simulation, 1 - Board Edit, 2 - Cursor Edit
        '''
        self.mode = n

    def mazify(self):
        '''Creates randomly generated maze'''
        self.searchActive = False
        self.board.mazify()

    def clear(self):
        '''Clears search (path and visited nodes) visuals from board'''
        self.searchActive = False
        self.board.clearPath()

    def quit(self):
        '''Quits program'''
        self.isRunning = False

