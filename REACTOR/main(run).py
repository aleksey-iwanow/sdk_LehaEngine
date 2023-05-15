from settings import *
from framework_LehaEngine import *


class Main:
    def __init__(self):
        self.RUN = True

        self.win = Window([1707, 1067], "REACTOR", full_sc=True, fps=31)
        self.fps_txt = self.win.find_object_of_name("fps_text")
        self.lep_1 = self.win.find_object_of_name("lep_1")
        self.lep_2 = self.win.find_object_of_name("lep_2")
        self.lep_3 = self.win.find_object_of_name("lep_3")
        self.lep_4 = self.win.find_object_of_name("lep_4")
        self.button_buy = self.win.find_object_of_name("button_buy")
        self.electro_main = self.win.find_object_of_name("electro_main")
        self.button_set_line = self.win.find_object_of_name("button_set_line")
        self.win.add_object_in_camera(self.win.find_object_of_name("camera"))
        self.list_leps = [self.lep_1, self.lep_3, self.lep_2, self.lep_4]
        self.lep_1.argument = [[630, 530], [self.electro_main.pos[0] - 70, self.electro_main.pos[1] - 110]]
        self.lep_3.argument = [[self.electro_main.pos[0] - 70, self.electro_main.pos[1] - 110]]
        self.lep_2.argument = [[self.lep_4.pos[0], self.lep_4.pos[1] - 65]]
        self.lep_4.argument = [[self.lep_3.pos[0], self.lep_3.pos[1] - 65]]
        self.b_obj = None
        self.b_obj_collision = None
        self.is_settings_line = False

    def start_after(self):
        if get_start():
            self.button_buy.Button.set_func(lambda: self.create_building(self.lep_1))
            self.button_set_line.Button.set_func(lambda: self.set_line())

    def set_line(self):
        self.is_settings_line = True

    def draw_lines(self):
        for i in self.list_leps:
            if i.argument:
                for j in i.argument:
                    leha.draw.line(self.win.window, (240, 240, 240), (i.rectpos[0], i.rectpos[1] - 65), (j[0] + self.win.camera.pos[0], j[1] + self.win.camera.pos[1]), 2)
        if self.b_obj_collision:
            px = self.b_obj.rectpos[0]
            py = self.b_obj.rectpos[1]
            sx = self.b_obj.size[0]
            sy = self.b_obj.size[1]

            leha.draw.line(self.win.window, (200, 20, 20), (px - sx / 2, py - sy / 2), (px - sx / 2, py + sy / 2), 4)
            leha.draw.line(self.win.window, (200, 20, 20), (px + sx / 2, py - sy / 2), (px + sx / 2, py + sy / 2), 4)
            leha.draw.line(self.win.window, (200, 20, 20), (px - sx / 2, py - sy / 2), (px + sx / 2, py - sy / 2), 4)
            leha.draw.line(self.win.window, (200, 20, 20), (px - sx / 2, py + sy / 2), (px + sx / 2, py + sy / 2), 4)

    def create_building(self, obj):
        self.b_obj = self.win.copy(obj, pos=[50000, 40000], index=len(self.win.list_objects))

    def check_events(self):
        for event in leha.event.get():
            if event.type == leha.QUIT:
                self.RUN = False
            elif event.type == leha.MOUSEBUTTONDOWN:
                self.check_build()

    def check_build(self):
        if self.b_obj and not self.b_obj_collision:
            self.win.set_index(self.b_obj, self.win.get_index(self.lep_1) + 1)
            self.b_obj = None

    def update_after(self):
        pass

    def update_before(self):

        mv = [0, 0]
        if input_k(leha.K_w):
            mv[1] -= 8 / self.win.scale_factor
        elif input_k(leha.K_s):
            mv[1] += 8 / self.win.scale_factor
        if input_k(leha.K_a):
            mv[0] += 8 / self.win.scale_factor
        elif input_k(leha.K_d):
            mv[0] -= 8 / self.win.scale_factor
        self.win.camera.move(mv, 1, not_collision=True)
        if self.b_obj:
            self.b_obj_collision = self.b_obj.collision()
            self.b_obj.pos = [leha.mouse.get_pos()[0] - self.win.camera.pos[0],leha.mouse.get_pos()[1] - self.win.camera.pos[1]]

    def run(self):
        while self.RUN:
            self.check_events()

            self.win.fill_window()
            self.update_before()
            self.win.update_game_objects()
            self.update_after()
            self.draw_lines()
            self.fps_txt.Text.set_text("fps:" + str(round(self.win.get_fps(), 2)))
            self.start_after()
            self.win.update_window()

        quit_app()


if __name__ == "__main__":
    main = Main()
    main.run()
