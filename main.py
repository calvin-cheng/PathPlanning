import curses
from objects.Game import Game
from objects.Board import Board
from objects.Menu import Menu, Radio, Button

def main(stdscr):
    h, w = stdscr.getmaxyx()
    if h < 39 and w < 136:
        curses.endwin()
        print('Window must be larger than 136 by 39!')
        print('Current size: {} by {}.'.format(w, h))
        return

    board = Board(18, 22)
 
    game = Game(board, stdscr)
    game.start()

curses.wrapper(main)

