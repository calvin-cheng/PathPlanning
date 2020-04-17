import curses
import curses.panel

class Menu:
    def __init__(self, x, y, width, height, items, stdscr):
        self.screen = stdscr
        self.window = stdscr.subwin(height, width, y, x)
        self.panel = curses.panel.new_panel(self.window) 
        self.panel.hide()
        curses.panel.update_panels()

        self.items = items
        self.pos = 0
        while isinstance(self.items[self.pos], (Text, Spacer)):
            self.pos += 1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        y = 0
        for idx, item in enumerate(self.items):
            selected = True if idx == self.pos else False
            item.display(2, 1+y, item.width, item.height, selected, self.window)
            y += item.height
        self.window.box()
        self.window.refresh()

    def nav(self, n):
        if self.items[self.pos].focus(n):
            self.pos += n
            self.pos = self.pos % len(self.items)
            while isinstance(self.items[self.pos], (Text, Spacer)):
                self.nav(n)
        else:
            self.items[self.pos].nav(n)

    def navX(self, n):
        try:
            self.items[self.pos].navX(n)
        except:
            pass


    def select(self):
        self.items[self.pos].run()

class RadioGroup:
    def __init__(self, radios, width):
        self.radios = radios
        self.pos = 0
        
        self.width = width
        self.height = len(self.radios) * 2 + 1

    def display(self, x, y, width, height, selected, screen):
        for idx, radio in enumerate(self.radios):
            radio_selected = True if selected and idx == self.pos else False
            radio.display(x, 1+y+idx*2, radio_selected, screen)

    def nav(self, n):
        self.pos += n
        if self.pos < 0:
            self.pos = 0
        elif self.pos >= len(self.radios):
            self.pos = len(self.radios) - 1

    def focus(self, n):
        '''Returns True if key up/down allowed to nav away from button'''
        if n == 1 and self.pos == len(self.radios) - 1:
            return True
        elif n == -1 and self.pos == 0:
            return True
        else:
            return False

class RadioGroupSingle(RadioGroup):
    def __init__(self, radios, width):
        super().__init__(radios, width)
        self.state = 0
        self.radios[self.pos].state = True
        
    def run(self):
        if self.radios[self.pos].state == False:
            for radio in self.radios:
                radio.state = False
            self.radios[self.pos].run()
            self.state = self.pos

class RadioGroupMultiple(RadioGroup):
    def run(self):
        self.radios[self.pos].run()

class Radio:
    def __init__(self, text, state=False):
        self.text = text
        self.state = state

    def display(self, x, y, selected, screen):
        attr = curses.A_REVERSE if selected else curses.A_NORMAL
        screen.addstr(y, x, self.string(), attr)

    def string(self):
        radio = '(o) ' if self.state else '( ) '
        return radio + self.text

    def run(self):
        self.state = not(self.state)

    def focus(self, n):
        '''Returns True if key up/down allowed to nav away from button'''
        return True

class Button:
    def __init__(self, text, fun, width, height):
        self.text = text
        self.fun = fun
        self.width = width
        self.height = height

    def display(self, x, y, width, height, selected, screen):
        attr = curses.A_REVERSE if selected else curses.A_NORMAL
        top = u'\u250c' + u'\u2500' * (width - 2) + u'\u2510'
        screen.addstr(y, x, top, attr)
        for i in range(height-2):
            if i == (height-2)//2:
                string = u'\u2502' + '{:^{w}}'.format(self.text, w = width - 2) + u'\u2502'
            else:
                string = u'\u2502' + ' ' * (width - 2) + u'\u2502'
            screen.addstr(y+1+i, x, string, attr)
        bottom = u'\u2514' + u'\u2500' * (width - 2) + u'\u2518'
        screen.addstr(y+i+2, x, bottom, attr)

    def string(self):
        return self.text

    def run(self):
        self.fun()

    def focus(self, n):
        '''Returns True if key up/down allowed to nav away from button'''
        return True

class ButtonGroup:
    def __init__(self, buttons, width):
        self.buttons = buttons
        self.pos = 0
        self.width = width
        self.height = max([button.height for button in buttons])

    def display(self, x, y, width, height, selected, screen):
        dx = 2
        for idx, button in enumerate(self.buttons):
            button_selected = True if selected and idx == self.pos else False
            button.display(dx, y, button.width, button.height, button_selected, screen)
            dx += button.width + 1

    def run(self):
        self.buttons[self.pos].run()

    def navX(self, n):
        self.pos += n
        self.pos = self.pos % len(self.buttons)

    def focus(self, n):
        '''Returns True if key up/down allowed to nav away from button'''
        return True


class Text:
    def __init__(self, text, width):
        self.text = text
        self.width = width
        self.height = 1

    def focus(self, n):
        return True

class Spacer:
    def __init__(self, height):
        self.height = height
        self.width = 0

    def display(self, x, y, width, height, selected, screen):
        return

    def focus(self, n):
        return True
        
class Heading(Text):
    def display(self, x, y, width, height, selected, screen):
        sep = ' ' + '–' * (width - len(self.text) - 1)
        screen.addstr(y, x, self.text+sep, curses.A_BOLD)

class Title(Text):
    def display(self, x, y, width, height, selected, screen):
        string = ' {} '.format(self.text.upper()).center(self.width, '=')
        screen.addstr(y, x, string, curses.A_BOLD)

    
