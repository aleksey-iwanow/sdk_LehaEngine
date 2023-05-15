from framework_LehaEngine import *


class Label:
    def __init__(self, gm):
        self.pos = gm.pos
        self.size = gm.size
        self.gm = gm


class MainWindow:
    def __init__(self, pos, name, code):
        self.pos = pos
        self.widgets = []
        self.widgets_app = []
        self.old_pos = []
        self.is_move = False

        self.title = win.create_object(f"title_calc_{code}", "None", self.pos, [550, 20])
        self.title.ColorBox = ColorBox('#1B1C1D')
        self.title.activeself = False

        self.button_close = win.create_object(f"button_close_calc_{code}", "None", [self.pos[0] - self.title.size[0] / 2 + 10, self.pos[1]], [16, 16])
        self.button_close.ColorBox = ColorBox('#A92328')
        self.button_close.Button = Button(f"run_function_from_code({code}, 'hide')", "#121212", "#121212", self.button_close)
        self.button_close.activeself = False

        self.name = name

        self.title_text = win.create_object(f"title_text_calc_{code}", "None", self.pos, [300, 20])
        self.title_text.Text = Text(self.name, 20, "#67D02F")
        self.title_text.activeself = False

        self.background = win.create_object(f"back_calc_{code}", "None", [self.pos[0], self.pos[1] + 200 + self.title.size[1] / 2], [550, 400])
        self.background.ColorBox = ColorBox('#110E0E')
        self.background.activeself = False
        self.delta_vec = []
        self.widgets.extend([self.background, self.title, self.title_text, self.button_close])

    def moving(self):
        if MOUSEBUTTONDOWN[0]:
            self.old_pos = [get_mouse_pos()[0], get_mouse_pos()[1]]
            self.delta_vec = [self.pos[0] - self.old_pos[0], self.pos[1] - self.old_pos[1]]
            if leha.Rect.collidepoint(
                    leha.Rect(self.title.pos[0] - self.title.size[0] / 2, self.pos[1] - self.title.size[1] / 2,
                              self.title.size[0], self.title.size[1]), self.old_pos[0], self.old_pos[1]):
                self.is_move = True

        if not leha.mouse.get_pressed()[0]:
            self.is_move = False

        if leha.mouse.get_pressed()[0] and self.is_move:
            if ISCLICK[0]:
                ISCLICK[0] = True
                for w in self.widgets:
                    w.set_index(len(self.widgets) - 1)
            self.pos = [get_mouse_pos()[0] + self.delta_vec[0], get_mouse_pos()[1] + self.delta_vec[1]]

    def show(self):
        for widget in self.widgets:
            widget.activeself = True

    def hide(self):
        for widget in self.widgets:
            widget.activeself = False

    def update_(self):
        self.moving()
        self.move_()

    def move_(self):
        self.title.pos = self.pos
        self.title_text.pos = self.pos
        self.background.pos = [self.pos[0], self.pos[1] + 200 + self.title.size[1] / 2]
        self.button_close.pos = [self.pos[0] - self.title.size[0] / 2 + 10, self.pos[1]]
        for w in self.widgets_app:
            w.gm.pos = [w.pos[0] + self.background.pos[0] - self.background.size[0] / 2 + w.size[0] / 2, w.pos[1] + self.background.pos[1]- self.background.size[1] / 2 + w.size[0] / 2]


debugs = []
MOUSEBUTTONDOWN = [False]
ISCLICK = [False]
win = Window([1707, 1067], "MYOS", full_sc=True)


def set_debug(debug):
    debugs.append(debug)


def get_debugs():
    return debugs


def set_mbd(value):
    MOUSEBUTTONDOWN.clear()
    MOUSEBUTTONDOWN.append(value)
