from functions import *


class Main:
    def __init__(self, pos):
        self.window = MainWindow(pos, "-= Дино =-", "dino")
        self.text_ = Label(win.create_object("text_test2", "None", [10, 10], [100, 20]))
        self.window.widgets.append(self.text_.gm)
        self.window.widgets_app.append(self.text_)
        self.text_.gm.Text = Text("тестовый текст", 20, '#232111')

    def update_app(self):
        pass


def start(args):
    global main
    set_debug(f'start{random.randrange(0, 9999)}')
    if not main:
        main = Main([500, 400])
    main.window.show()


def update(args):
    if main:
        main.window.update_()
        main.update_app()


main = None
