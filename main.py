import curses
import time
from objects.PathPlanners import Dijkstra, AStar
from objects.Board import Board

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    curses.use_default_colors()

    # (i, fg, bg), 0 reserved. fg, bg = -1 for default values
    curses.init_pair(1, -1, -1)  # Gap
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)    # Player
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN) # Goal
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW) # Path
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE) # Visited
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_CYAN) # Frontier

    h, w = stdscr.getmaxyx()
    m = Board(h//3, w//6)
    
    m.draw(stdscr)
    string = "(T)oggle | (M)azify | (C)lear path | (R)eset | (S)earch | (Q)uit"
    stdscr.addstr(h//2 + m.l//2, w//2 - len(string)//2, string,
                  curses.A_BOLD)

    player = True
    planner = 0

    while True:
        h, w = stdscr.getmaxyx()
        playerStatus = "Moving: START" if player else "Moving: GOAL "
        plannerStatus = "Path Planner: A-STAR  " if planner else "Path Planner: DIJKSTRA"
        stdscr.addstr(h//2 + m.l//2 + 1, 
                      w//2 - (len(playerStatus) + len('  |  ') + len(plannerStatus)) // 2, 
                      playerStatus + '  |  ' + plannerStatus, curses.A_BOLD)

        key = stdscr.getch()

        players = {True: m.player, False: m.goal}
        planners = {0: Dijkstra, 1: AStar}

        if key == curses.KEY_UP:
            m.moveNode(players[player], 'U')
            m.draw(stdscr)
        elif key == curses.KEY_DOWN:
            m.moveNode(players[player], 'D')
            m.draw(stdscr)
        elif key == curses.KEY_RIGHT:
            m.moveNode(players[player], 'R')
            m.draw(stdscr)
        elif key == curses.KEY_LEFT:
            m.moveNode(players[player], 'L')
            m.draw(stdscr)
        elif key == ord('q'):
            curses.curs_set(1)
            break
        elif key == ord('s'):
            m.clearPath()
            d = planners[planner](m)
            path = d.search(m.player, m.goal, stdscr)
            for node in path:
                i, j = node
                time.sleep(0.04)
                m.board[j][i] = 2
                m.draw(stdscr)
        elif key == ord('m'):
            m.mazify()
            m.draw(stdscr)
        elif key == ord('r'):
            m.generate()
            m.draw(stdscr)
        elif key == ord('c'):
            m.clearPath()
            m.draw(stdscr)
        elif key == ord('t'):
            player = not(player)
        elif key == ord(' '):
            planner = (planner + 1) % 2

curses.wrapper(main)



