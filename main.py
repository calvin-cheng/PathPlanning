import curses
import time
import random
from objects.PathPlanners import Djikstra, AStar
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
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_CYAN) # Marked

    h, w = stdscr.getmaxyx()
    m = Board(h//3, w//6)
    move = True # True: move player, False: move goal
    
    m.draw(stdscr)
    string = "(T)oggle | (M)azify | (C)lear path | (R)eset | (S)earch | (Q)uit"
    stdscr.addstr(h//2 + m.l//2, w//2 - len(string)//2, string,
                  curses.A_BOLD)

    while True:
        h, w = stdscr.getmaxyx()
        status = "Moving: START" if move else "Moving: GOAL "
        stdscr.addstr(h//2 + m.l//2 + 1, w//2 - len(status)//2, status,
                      curses.A_BOLD)
        if move:
            toMove = m.player
        else:
            toMove = m.goal
            
        key = stdscr.getch()

        if move:
            toMove = m.player
        else:
            toMove = m.goal

        if key == curses.KEY_UP:
            m.moveNode(toMove, 'U')
            m.draw(stdscr)
        elif key == curses.KEY_DOWN:
            m.moveNode(toMove, 'D')
            m.draw(stdscr)
        elif key == curses.KEY_RIGHT:
            m.moveNode(toMove, 'R')
            m.draw(stdscr)
        elif key == curses.KEY_LEFT:
            m.moveNode(toMove, 'L')
            m.draw(stdscr)
        elif key == ord('q'):
            curses.curs_set(1)
            break
        elif key == ord('s'):
            m.clearPath()
            d = Djikstra(m)
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
            move = not(move)

        if m.checkWin():
            stdscr.clear()
            string = "You win, noice!"
            stdscr.addstr(h//2, w//2 - len(string)//2, string)
            stdscr.refresh()
            time.sleep(1.5)
            break

curses.wrapper(main)



