import curses
from objects.Game import Game
from objects.Board import Board
from objects.Menu import Menu, Radio, Button

def main(stdscr):
    h, w = stdscr.getmaxyx()
    H_LIM, W_LIM = 38, 120
    if h < H_LIM and w < W_LIM:
        curses.endwin()
        print()
        print('Window must be at least {} by {}!'.format(H_LIM, W_LIM))
        print('Current size: {} by {}.'.format(w, h))
        return
    else:
        board = Board(18, 22)
        game = Game(board, stdscr)
        game.start()

curses.wrapper(main)

