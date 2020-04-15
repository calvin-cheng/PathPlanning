import curses
import curses.panel

class Menu:
    def __init__(self, x, y, items, stdscr):
        self.screen = stdscr
        self.window = stdscr.subwin(curses.LINES - 2, 41, y, x)
        self.panel = curses.panel.new_panel(self.window)
        self.panel.hide()
        curses.panel.update_panels()

        self.items = items
        self.pos = 0

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        for idx, item in enumerate(self.items):
            if self.pos == idx:
                attr = curses.A_BOLD | curses.A_REVERSE
            else:
                attr = curses.A_BOLD
            self.window.addstr(3+idx, 2, item.string(), attr)
        self.window.addstr(3+idx+1, 2, '') # Prevent underline hiding
        self.window.box()
        self.window.refresh()

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

    
