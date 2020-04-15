import curses

class Menu:
    def __init__(self, x, y, items, stdscr):
        self.window = stdscr.subwin(curses.LINES - 2, 41, y, x)
        self.items = items
        self.pos = 0

    def nav(self, n):
        self.pos += n
        self.pos = self.pos % len(self.items)

    def select(self):
        self.items[self.pos].run()


class Radio:
    def __init__(self, text, state=False):
        self.text = text
        self.state = state

    def string(self):
        radio = '(o) ' if self.state else '( ) '
        return radio + self.text

    def run(self):
        self.state = not(self.state)


class Button:
    def __init__(self, text, fun):
        self.text = text
        self.fun = fun

    def string(self):
        return self.text

    def run(self):
        self.fun()

    
