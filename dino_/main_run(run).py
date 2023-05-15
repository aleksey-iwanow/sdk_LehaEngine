from framework_LehaEngine import *


class Bullet:
    def __init__(self, gameObject):
        self.speed = 20
        self.gameObject = win.copy(gameObject)
        self.gameObject.pos = [pos_bullet.parent.pos[0] + pos_bullet.pos[0], pos_bullet.parent.pos[1] + pos_bullet.pos[1]]
        self.delta = 100 + cur

    def move_(self):
        if cur < self.delta:
            self.gameObject.pos[1] = pos_bullet.parent.pos[1] + pos_bullet.pos[1]
        self.gameObject.pos[0] += self.speed
        self.check_bullet()

    def remove_bullet(self):
        win.list_objects.remove(self.gameObject)
        bullets.remove(self)

    def check_bullet(self):
        if self.gameObject.pos[0] - self.gameObject.size[0] // 2 > win.width_win:
            self.remove_bullet()
        else:
            coll = self.gameObject.collision()
            if coll and coll.type_ == "cactus":
                self.remove_bullet()
                coll.set_opacity(0)
                vz = win.copy(vzriv)
                vz.set_parent(coll)
                vz.pos = [0, 0]

                coll.is_collision = False


def set_argument(args):
    obj, arg = args
    obj.argument = arg


def spawn_object(args):
    obj, range_, random_time = args
    if obj.argument <= cur and obj.pos[0] < -obj.size[0]:
        obj.argument = cur + random.randrange(random_time[0], random_time[1])
        obj.pos = [1707 + obj.size[0], random.randrange(range_[0], range_[1])]
        while obj.collision():
            obj.pos = [1707 + obj.size[0], random.randrange(range_[0], range_[1])]


def spawn_cactus():
    global delta_spawn_cactus, delta_spawn_ak
    if cur > delta_spawn_ak:
        delta_spawn_ak = cur + random.randrange(TIME_SPAWN_AK[0], TIME_SPAWN_AK[1])
        delta_spawn_cactus = cur + random.randrange(TIME_SPAWN_CACTUS[0], TIME_SPAWN_CACTUS[1])
        cactus_copy.remove(ak_copy), cactus_list.append(ak_copy)

    elif cur > delta_spawn_cactus and len(cactus_copy) > 0:
        delta_spawn_cactus = cur + (random.randrange(TIME_SPAWN_CACTUS[0], TIME_SPAWN_CACTUS[1]) * (NORM_SPEED / SPEED))
        nm, c = "ak_1", None
        while nm == "ak_1":
            c = cactus_copy[random.randrange(0, len(cactus_copy))]
            nm = c.name
        cactus_copy.remove(c), cactus_list.append(c)


def jump():
    global delta_time_a, CUR_SPEED_JUMP, A, is_jump, IN_HEIGHT
    if delta_time_a < cur:
        delta_time_a = cur + TIME_A
        CUR_SPEED_JUMP -= A
        if IN_HEIGHT:
            IN_HEIGHT = False
        else:
            CUR_SPEED_JUMP -= A
    if not IN_HEIGHT:
        if dino.pos[1] <= 200:
            delta_time_a = cur + TIME_A
            IN_HEIGHT = True
        if is_jump:
            dino.pos[1] -= CUR_SPEED_JUMP

        if dino.pos[1] > 970 - SPEED_JUMP and is_jump:
            CUR_SPEED_JUMP = SPEED_JUMP
            run_anim.active, jump_anim.active, is_jump = True, False, False


def clear_():
    global score, cactus_list, cactus_copy
    score = 0
    cactus_copy = [ak_copy]
    cactus_copy += win.find_objects_of_parameter('cactus', 'type_')
    for c in cactus_copy:
        c.pos[0] = 1750 + c.size[0] // 2

    cactus_list = []


def update_score():
    global delta_time_score, score, SPEED
    if cur > delta_time_score and not start:
        delta_time_score = cur + 100
        score += 1
        if not score % 100 and SPEED < 20:
            SPEED += 1
        sc_ui.Text.set_text(f'{"0" * (6 - len(str(score)))}{str(score)}')
        hi_ui.Text.set_text(f'HI {"0" * (6 - len(str(high)))}{str(high)}')


def put_away_ak():
    global bandana_active, active_ak
    active_ak = False
    if not start:
        destroy_source.play()
    txt_bul.Text.set_color("#111111")
    ak.activeself = False
    bandana_active = False
    dont_active.activeself = True


def get_ak():
    global bandana_active, active_ak
    active_ak = True
    prz_source.play()
    txt_bul.Text.set_color("#5C5C5C")
    ak.activeself = True
    bandana_active = True
    dont_active.activeself = False


def move_objects():
    for o in objects_:
        if o.type_ == 'win':
            o.move([-2 * FPS / (fp if fp > 0 else FPS), 0], 1)
        else:
            o.move([-CUR_SPEED, 0], 1)


def move_road():
    for road in roads:
        road.pos[0] -= CUR_SPEED
        if road.pos[0] <= -road.size[0] // 2:
            road.pos[0] = round(road.size[0] * 1.5)


def move_cactus():
    for c in cactus_list:
        c.pos[0] -= CUR_SPEED
        if c.pos[0] < -c.size[0] // 2:
            c.pos[0] = 1750 + c.size[0] // 2
            c.set_opacity(1)
            c.is_collision = True
            cactus_copy.append(c), cactus_list.remove(c)


def move_bullets():
    for b in bullets:
        b.move_()


def set_bullets(num):
    global bullets_num
    bullets_num = num
    txt_bul.Text.set_text(f'{bullets_num}/30')


def update_scene():
    global start, delta_start, high, bullets_num

    move_objects(), move_road(), move_cactus(), move_bullets()

    coll = dino.collision()
    if coll:
        if coll.type_ == "cactus":
            start = True
            back_source.stop(), back2_source.stop(), dead_source.play()
            delta_start = 200 + cur
            dino.size = [188, 176]
            if sit_anim.active:
                dino.pos[1] -= 30
            run_anim.active, jump_anim.active, sit_anim.active, dead_anim.active = False, False, False, True
            text_dead.activeself, text_start.activeself = True, True
            if score > high:
                high = score
        elif coll.type_ == "ak":
            coll.pos[0] = 1750 + coll.size[0] // 2
            cactus_list.remove(ak_copy), cactus_copy.append(ak_copy)
            set_bullets(30), get_ak()


SPEED, SPEED_JUMP = 10, 20
NORM_SPEED = 12
CUR_SPEED, CUR_SPEED_JUMP = SPEED, SPEED_JUMP
FPS = 80
A = 1
TIME_A = 50
delta_time_a = TIME_A
delta_time_score = 100
delta_ak_shoot = 200
delta_start = 200
RANGE_SPAWN_WINDOW = [50, 400]
TIME_SPAWN_CACTUS = [1600, 2600]
TIME_SPAWN_AK = [20000, 30000]
delta_spawn_cactus = TIME_SPAWN_CACTUS[0]
delta_spawn_ak = TIME_SPAWN_AK[0]
IN_HEIGHT = False
active_ak = True
# C:\\Users\\aleks\\PycharmProjects\\sdk___\\
win = Window([1707, 1067], "dino_", full_sc=True, fps=80)
set_caption("DINO")
dino = win.find_object_of_name('dino')
ak = win.find_object_of_name('ak')
ak_copy = win.find_object_of_name('ak_1')
bullet_copy = win.find_object_of_name('bullet_copy')
bullets = []

bnd = win.find_object_of_name('bandana')
ak.set_parent(dino)
bnd.set_parent(dino)

text_start, text_dead, text_game = win.find_object_of_name('text_start'), win.find_object_of_name('text_dead'), \
                                   win.find_object_of_name('text_game')
pos_bullet = win.find_object_of_name('position_bullet')
pos_bullet.set_parent(dino)
dont_active = win.find_object_of_name('dont_active')
vzriv = win.find_object_of_name('vzriv')

sc_ui, hi_ui = win.find_object_of_name('score_ui'), win.find_object_of_name('high_score_ui')
high = 0
score = 0

txt_bul = win.find_object_of_name('text_bullets')
roads = [win.find_object_of_name('road_1'), win.find_object_of_name('road_2')]
w = win.find_object_of_name('win_1')

cur = 0
bullets_num = 0

is_jump = False
start = True
bandana_active = False
win.update_all()

# Анимации динозавра
sit_anim, run_anim, jump_anim, dead_anim, idle_anim = dino.find_animation('sit'), dino.find_animation('run'), \
                                                      dino.find_animation('jump'), dino.find_animation('dead'), \
                                                      dino.find_animation('idle')
sr = win.find_object_of_name('source')
# Анимации оружия
shoot_anim_ak, idle_anim_ak = ak.find_animation('shoot'), ak.find_animation('idle')
# звук прыжка
jump_source = dino.find_source('jump')
# фоновый звук
back_source = sr.find_source('back')
back2_source = sr.find_source('back_2')
# звук выстрела
shoot_source = ak.find_source('shoot')
# звук уничтожения автомата
destroy_source = ak.find_source('destroy')
# звук перезарядки
prz_source = ak.find_source('perezaradka')
# звук смерти
dead_source = sr.find_source('dead')
objects_ = win.find_objects_of_parameter("win", "type_")

while check_run():
    win.fill_window((255, 255, 255))
    fp = win.get_fps()
    cur = get_current_time()

    CUR_SPEED = round(SPEED * FPS / (fp if fp > 0 else FPS))
    if objects_ and not start:
        spawn_cactus(), update_scene(), jump()

    if input_k(leha.K_SPACE):
        if start and delta_start < cur:
            delta_start, delta_spawn_cactus, delta_spawn_ak = 200 + cur, TIME_SPAWN_CACTUS[0] + cur, cur
            start = False
            SPEED = 10
            set_bullets(0)
            for b in bullets:
                b.remove_bullet()
            back_source.play(), clear_()
            run_anim.active, idle_anim.active, dead_anim.active = True, False, False
            text_dead.activeself, text_start.activeself, text_game.activeself = [False for b in range(3)]
        elif not is_jump:
            is_jump = True
            jump_source.play()
            run_anim.active, sit_anim.active, jump_anim.active = False, False, True
            dino.size = [188, 176]
            dino.pos[1] = 970
            delta_time_a = cur + TIME_A
            CUR_SPEED_JUMP = SPEED_JUMP
    elif input_k(leha.K_DOWN) and not is_jump and not start:
        sit_anim.active, run_anim.active, jump_anim.active, bandana_active = True, False, False, False
        dino.size = [236, 120]
        dino.pos[1] = 1000
    elif not start and not is_jump:
        dino.size = [188, 176]
        dino.pos[1] = 970
        sit_anim.active, run_anim.active = False, True

    if input_k(leha.K_w) and not start:
        if bullets_num > 0:
            active_ak, shoot_anim_ak.active, idle_anim_ak.active = True, True, False
            if cur > delta_ak_shoot:
                delta_ak_shoot = cur + 200
                shoot_source.stop(), shoot_source.play()
                bullets.append(Bullet(bullet_copy)), set_bullets(bullets_num - 1)
    else:
        shoot_anim_ak.active, idle_anim_ak.active = False, True

    if active_ak and bullets_num <= 0:
        put_away_ak()
    elif bullets_num > 0 and not back2_source.is_playing and not start:
        back_source.stop(), back2_source.play()
    elif bullets_num <= 0 and back2_source.is_playing and not start:
        back_source.play(), back2_source.stop()

    bnd.activeself = bandana_active
    update_score(), win.update_game_objects(), win.update_window()
quit_app()
