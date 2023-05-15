from functions import *


class Main:
    def __init__(self, pos):
        self.window = MainWindow(pos, "-= Калькулятор =-", "calculator")
        self.text_ = Label(win.create_object("text_test", "None", [10, 10], [100, 20]))
        self.image_ = Label(win.create_object("image_test", "images/6oa.gif", [20, 20], [100, 100]))

        self.list_obj = [self.text_, self.image_]

        self.window.widgets.extend([a.gm for a in self.list_obj])
        self.window.widgets_app.extend(self.list_obj)
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


