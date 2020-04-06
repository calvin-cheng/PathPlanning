import curses
import time
import random
from objects.PathPlanners import Djikstra
from objects.Board import Board

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    curses.use_default_colors()

    # (i, fg, bg), 0 reserved. fg, bg = -1 for default values
    curses.init_pair(1, -1, -1)  # Gap
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)    # Player
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN) # Goal
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW) # Path

    h, w = stdscr.getmaxyx()
    m = Board(h//3, w//6)
    
    m.draw(stdscr)
    string = "(M)azify | (R)eset | (S)earch | (Q)uit"
    stdscr.addstr(h//2 + m.l//2, w//2 - len(string)//2, string,
                  curses.A_BOLD)

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
            m.clearPath()
            d = Djikstra(m)
            path = d.search(m.player, m.goal)
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

        if m.checkWin():
            stdscr.clear()
            string = "You win, noice!"
            stdscr.addstr(h//2, w//2 - len(string)//2, string)
            stdscr.refresh()
            time.sleep(1.5)
            break

curses.wrapper(main)



