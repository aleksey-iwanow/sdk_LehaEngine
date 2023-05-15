from functions import *


def select_(gm):
    if leha.Rect.collidepoint(leha.Rect(gm.pos[0] - gm.size[0] / 2, gm.pos[1] - gm.size[1] / 2, gm.size[0], gm.size[1]), get_mouse_pos()[0], get_mouse_pos()[1]):
        gm.opacity = 0.5
    else:
        gm.opacity = 0


class App:
    def __init__(self, title, gameObject, text, func, pos_, args=None):
        self.gm = win.copy(gameObject)
        self.txt = win.copy(text)
        self.title = title
        win.update_all()
        self.func, self.args = func, args

        self.txt.Text.set_text(title)
        self.pos = pos_
        self.old_pos = [0, 0]
        self.is_move = False
        self.size = [80, 80]

    def update_(self):
        self.update_pos()
        run_function_from_code(self.title.lower(), "update", self.args)

    def check_collision(self):
        self.old_pos = [get_mouse_pos()[0], get_mouse_pos()[1]]
        if leha.Rect.collidepoint(
                leha.Rect(self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2,
                          self.size[0], self.size[1]), self.old_pos[0], self.old_pos[1]):
            run_function_from_code(self.title.lower(), self.func, self.args)
            self.is_move = True

    def draw(self):
        leha.draw.rect(win.window, (20, 120, 20, 20), (
        self.pos[0] - self.size[0] / 2 - 10, self.pos[1] - self.size[0] / 2, self.size[0] + 20,
        self.size[1]), 3)
        self.pos = [get_mouse_pos()[0], get_mouse_pos()[1]]

    def update_pos(self):
        self.gm.pos = self.pos
        self.txt.pos = [self.pos[0], self.pos[1] + 30]


main_button = win.find_object_of_name('button_main')
panel_os = win.find_object_of_name('panel_os')
debug_message = win.find_object_of_name('message')
pn_deb = win.find_object_of_name('panel_debug')

but1 = win.find_object_of_name('button1')
but1.parent = panel_os
but2 = win.find_object_of_name('button2')
but2.parent = panel_os
center_line = win.find_object_of_name('center_line')
bottom_line = win.find_object_of_name('bottom_line')
left_line = win.find_object_of_name('left_line')
right_line = win.find_object_of_name('right_line')

messages = []
for i in range(7):
    d = win.copy(debug_message)
    d.pos = [pn_deb.pos[0], i * d.size[1] + pn_deb.pos[1] - pn_deb.size[1] / 2 + d.size[1] / 2]
    messages.append(d)

center_line.parent, bottom_line.parent, left_line.parent, right_line.parent = panel_os, panel_os, panel_os, panel_os

apps = [App('Calculator', win.find_object_of_name('app'), win.find_object_of_name('text'), "start", [200, 200]),
        App('Dino', win.find_object_of_name('app'), win.find_object_of_name('text'), "start", [200, 400])]

while check_run():
    ln_d = len(debugs)
    win.fill_window(), win.update_game_objects()

    set_mbd(False)
    for event in leha.event.get():
        if event.type == leha.MOUSEBUTTONDOWN:
            set_mbd(True)

    index_ = 0
    for i in range((ln_d - 7) if ln_d > 7 else 0, ln_d):
        messages[index_].Text.set_text(debugs[i])
        index_ += 1

    for app in apps:
        app.update_()
        if MOUSEBUTTONDOWN[0]:
            app.check_collision()

        if not leha.mouse.get_pressed()[0]:
            app.is_move = False

        if leha.mouse.get_pressed()[0] and app.is_move:
            app.draw()

    select_(main_button)

    set_caption("fps:" + str(round(win.get_fps(), 2)))
    win.update_window()

quit_app()
