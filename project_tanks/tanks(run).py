from framework_LehaEngine import *
from move_ import func_moving


class Enemy:
    def __init__(self, game_obj, hp, tanks):
        self.health = hp
        self.game_object = game_obj
        self.pos_current = None
        self.move_fact = 1
        self.is_change_move = False
        self.old_vec = []
        self.tanks = tanks

    def check_hp(self):
        if self.health <= 0:
            self.tanks.win.list_objects.remove(self.game_object)
            self.tanks.list_enemy.remove(self)
            num = int(self.tanks.score_text.text.split(':')[-1])
            self.tanks.score_text.text = f"score:{num + 1}"

            return False
        return True

    def move_(self):
        if self.pos_current:
            if self.game_object.pos != self.pos_current.pos:
                if abs(self.pos_current.pos[0] - self.game_object.pos[0]) > abs(self.pos_current.pos[1] - self.game_object.pos[1]):
                    if self.pos_current.pos[0] > self.game_object.pos[0]:
                        vec = [1, 0]
                        self.game_object.angle = 270
                    else:
                        vec = [-1, 0]
                        self.game_object.angle = 90
                else:
                    if self.pos_current.pos[1] > self.game_object.pos[1]:
                        vec = [0, -1]
                        self.game_object.angle = 180
                    else:
                        vec = [0, 1]
                        self.game_object.angle = 0
                b = self.game_object.collision()
                if not (b and b.name == self.tanks.tank_.name):
                    self.game_object.move(vec, 1)
                    self.is_change_move = True
                    self.old_vec = [-vec[0], -vec[1]]
                else:
                    if self.is_change_move:
                        if self.tanks.positionsEnemy.index(self.pos_current) + 1 == len(self.tanks.positionsEnemy):
                            self.pos_current = self.tanks.positionsEnemy[0]
                        self.is_change_move = False
                        self.move_fact = self.move_fact * -1
                        self.pos_current = self.tanks.positionsEnemy[self.tanks.positionsEnemy.index(self.pos_current) + self.move_fact]
                        self.game_object.move(self.old_vec, 1)
            else:
                if self.tanks.positionsEnemy.index(self.pos_current) + 1 == len(self.tanks.positionsEnemy):
                    self.pos_current = self.tanks.positionsEnemy[0]
                else:
                    self.pos_current = self.tanks.positionsEnemy[self.tanks.positionsEnemy.index(self.pos_current) + self.move_fact]
        elif len(self.tanks.positionsEnemy) > 0:
            self.pos_current = self.tanks.positionsEnemy[0]


class MainClass:
    def __init__(self):
        self.win = Window([1000, 650], "project_tanks", (0, 0), 100)
        self.win.find_ui_of_name('buttonplay').set_functions(['engine.set_scene(1)'])
        self.bullet_copy = None
        self.tank_ = None
        self.score_text = None
        self.start_ = True
        self.start_2 = True
        self.positionsEnemy = []
        self.pos_tp = []
        self.old_vec = []
        self.bullets = []
        self.list_enemy = []
        self.speed_shoot = 13

        while check_run():
            if self.win.index_scene_now == 1:
                if self.start_2:
                    self.start_2 = False
                    self.bullet_copy = self.win.find_object_of_name('bullet_copy')
                    self.tank_ = self.win.find_object_of_name('tankMain')
                    self.score_text = self.win.find_ui_of_name('ScoreText')
                    for en_ in self.win.find_objects_of_parameter('Enemy', 'type_'):
                        self.list_enemy.append(Enemy(en_, 100, self))
                        en_.angle = 270

                    self.positionsEnemy = self.win.find_debug_objects_of_parameter('PosMoving', 'type_')

                func_moving(self)
            self.win.fill_window()
            self.win.update_game_objects()
            set_caption(f'fps: {str(round(self.win.get_fps(), 2))}')
            self.win.update_window()

        quit_app()


main_class = MainClass()
