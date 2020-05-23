import curses
from objects.Game import Game
from objects.Board import Board

windowTooSmall = False
def main(stdscr):
    global windowTooSmall
    h, w = stdscr.getmaxyx()
    H_LIM, W_LIM = 39, 120
    if h < H_LIM or w < W_LIM:
        windowTooSmall = True
        curses.endwin()
    else:
        board = Board(18, 22)
        game = Game(board, stdscr)
        game.start()

curses.wrapper(main)

#  Dialog after closing
if windowTooSmall:
    print('Window must be at least 39 by 120!')

