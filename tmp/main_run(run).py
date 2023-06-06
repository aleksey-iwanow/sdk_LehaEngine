import random
import psutil
from framework_LehaEngine import *


class Main:
    def __init__(self):
        self.RUN = True

        self.win = Window([300, 180], "REACTOR", fps=31)
        self.l_1 = [self.win.find_object_of_name("l_13"), self.win.find_object_of_name("l_19"), self.win.find_object_of_name("l_20")]
        self.l_2 = [self.win.find_object_of_name("l_14"),self.win.find_object_of_name("l_2"),self.win.find_object_of_name("l_5")]
        self.l_3 = [self.win.find_object_of_name("l_12"),self.win.find_object_of_name("l_4"),self.win.find_object_of_name("l_21")]
        self.l_4 = [self.win.find_object_of_name("l_11"),self.win.find_object_of_name("l_1"),self.win.find_object_of_name("l_3")]
        self.l_5 = [self.win.find_object_of_name("l_9"),self.win.find_object_of_name("l_16"),self.win.find_object_of_name("l_17")]
        self.l_6 = [self.win.find_object_of_name("l_15"),self.win.find_object_of_name("l_6"),self.win.find_object_of_name("l_8")]
        self.l_7 = [self.win.find_object_of_name("l_10"),self.win.find_object_of_name("l_7"),self.win.find_object_of_name("l_18")]
        self.num = 9

    def l1(self, num):
        self.l_1[num].ColorBox.set_color("#051505")
        self.l_2[num].ColorBox.set_color("#051505")
        self.l_3[num].ColorBox.set_color("#16DF25")
        self.l_4[num].ColorBox.set_color("#16DF25")
        self.l_5[num].ColorBox.set_color("#051505")
        self.l_6[num].ColorBox.set_color("#051505")
        self.l_7[num].ColorBox.set_color("#051505")

    def lp(self, num):
        self.l_1[num].ColorBox.set_color("#051505")
        self.l_2[num].ColorBox.set_color("#051505")
        self.l_3[num].ColorBox.set_color("#051505")
        self.l_4[num].ColorBox.set_color("#051505")
        self.l_5[num].ColorBox.set_color("#051505")
        self.l_6[num].ColorBox.set_color("#051505")
        self.l_7[num].ColorBox.set_color("#051505")

    def l0(self, num):
        self.l_1[num].ColorBox.set_color("#16DF25")
        self.l_2[num].ColorBox.set_color("#16DF25")
        self.l_3[num].ColorBox.set_color("#16DF25")
        self.l_4[num].ColorBox.set_color("#16DF25")
        self.l_5[num].ColorBox.set_color("#16DF25")
        self.l_6[num].ColorBox.set_color("#16DF25")
        self.l_7[num].ColorBox.set_color("#051505")

    def l2(self, num):
        self.l_1[num].ColorBox.set_color("#051505")
        self.l_2[num].ColorBox.set_color("#16DF25")
        self.l_3[num].ColorBox.set_color("#16DF25")
        self.l_4[num].ColorBox.set_color("#051505")
        self.l_5[num].ColorBox.set_color("#16DF25")
        self.l_6[num].ColorBox.set_color("#16DF25")
        self.l_7[num].ColorBox.set_color("#16DF25")

    def l3(self, num):
        self.l_1[num].ColorBox.set_color("#051505")
        self.l_2[num].ColorBox.set_color("#16DF25")
        self.l_3[num].ColorBox.set_color("#16DF25")
        self.l_4[num].ColorBox.set_color("#16DF25")
        self.l_5[num].ColorBox.set_color("#16DF25")
        self.l_6[num].ColorBox.set_color("#051505")
        self.l_7[num].ColorBox.set_color("#16DF25")

    def l4(self, num):
        self.l_1[num].ColorBox.set_color("#16DF25")
        self.l_2[num].ColorBox.set_color("#051505")
        self.l_3[num].ColorBox.set_color("#16DF25")
        self.l_4[num].ColorBox.set_color("#16DF25")
        self.l_5[num].ColorBox.set_color("#051505")
        self.l_6[num].ColorBox.set_color("#051505")
        self.l_7[num].ColorBox.set_color("#16DF25")

    def l5(self, num):
        self.l_1[num].ColorBox.set_color("#16DF25")
        self.l_2[num].ColorBox.set_color("#16DF25")
        self.l_3[num].ColorBox.set_color("#051505")
        self.l_4[num].ColorBox.set_color("#16DF25")
        self.l_5[num].ColorBox.set_color("#16DF25")
        self.l_6[num].ColorBox.set_color("#051505")
        self.l_7[num].ColorBox.set_color("#16DF25")

    def l6(self, num):
        self.l_1[num].ColorBox.set_color("#16DF25")
        self.l_2[num].ColorBox.set_color("#16DF25")
        self.l_3[num].ColorBox.set_color("#051505")
        self.l_4[num].ColorBox.set_color("#16DF25")
        self.l_5[num].ColorBox.set_color("#16DF25")
        self.l_6[num].ColorBox.set_color("#16DF25")
        self.l_7[num].ColorBox.set_color("#16DF25")

    def l7(self, num):
        self.l_1[num].ColorBox.set_color("#051505")
        self.l_2[num].ColorBox.set_color("#16DF25")
        self.l_3[num].ColorBox.set_color("#16DF25")
        self.l_4[num].ColorBox.set_color("#16DF25")
        self.l_5[num].ColorBox.set_color("#051505")
        self.l_6[num].ColorBox.set_color("#051505")
        self.l_7[num].ColorBox.set_color("#051505")

    def l8(self, num):
        self.l_1[num].ColorBox.set_color("#16DF25")
        self.l_2[num].ColorBox.set_color("#16DF25")
        self.l_3[num].ColorBox.set_color("#16DF25")
        self.l_4[num].ColorBox.set_color("#16DF25")
        self.l_5[num].ColorBox.set_color("#16DF25")
        self.l_6[num].ColorBox.set_color("#16DF25")
        self.l_7[num].ColorBox.set_color("#16DF25")

    def l9(self, num):
        self.l_1[num].ColorBox.set_color("#16DF25")
        self.l_2[num].ColorBox.set_color("#16DF25")
        self.l_3[num].ColorBox.set_color("#16DF25")
        self.l_4[num].ColorBox.set_color("#16DF25")
        self.l_5[num].ColorBox.set_color("#16DF25")
        self.l_6[num].ColorBox.set_color("#051505")
        self.l_7[num].ColorBox.set_color("#16DF25")

    def spellFunction(self, num):
        num = str(num).rjust(3, "p")
        for u in range(len(num)):
            eval(f"self.l{num[u]}({u})")

    def draw(self):
        self.spellFunction(123)

    def check_events(self):
        for event in leha.event.get():
            if event.type == leha.QUIT:
                self.RUN = False

    def run(self):
        while self.RUN:
            self.check_events()
            self.win.fill_window()
            self.win.update_game_objects()
            set_caption(f'fps: {str(round(self.win.get_fps(), 2))}')
            self.draw()
            self.win.update_window()
        quit_app()


if __name__ == "__main__":
    main = Main()
    main.run()
