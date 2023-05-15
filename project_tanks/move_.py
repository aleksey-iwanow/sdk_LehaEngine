from framework_LehaEngine import *


def shoot(wn, bull, name_tank):
    bl = False
    if bull.pos[0] == spawn_pos and bull.pos[1] == spawn_pos:
        bl = True

    if bl:
        tnk = wn.find_object_of_name(name_tank)
        bull.pos[0], bull.pos[1] = tnk.pos[0], tnk.pos[1]
        mvec = [0, 0]
        if tnk.angle == 0:
            mvec = [0, 6]
        elif tnk.angle == 90:
            mvec = [-6, 0]
        elif tnk.angle == 180:
            mvec = [0, -6]
        elif tnk.angle == 270:
            mvec = [6, 0]
        bull.old_vector_moving = mvec
        bull.angle = tnk.angle

    bull.move(bull.old_vector_moving, 1)


def create_bull(tanks):
    bl = tanks.win.create_object('bullet',
                                 tanks.bullet_copy.path,
                                 [spawn_pos, spawn_pos],
                                 tanks.bullet_copy.size,
                                 components=tanks.bullet_copy.components,
                                 indInsert=tanks.win.get_index(tanks.tank_))
    tanks.bullets.append(bl)


def find_enemy_of_game_obj(tanks, gm):
    for i in tanks.list_enemy:
        if i.game_object.name == gm.name:
            return i


def crt_anim_vz(tanks, x, y):
    tanks.win.create_animation(['images\\vzriv1.png', 'images\\vzriv2.png', 'images\\vzriv3.png'], [x, y], [50, 50], 60, False, is_deleted=True)


def func_moving(tanks):
    global speed_shoot
    move_vec = [0, 0]

    if input_k(leha.K_w):
        if tanks.tank_.inWindowUp(50):
            move_vec[1] += 2
        tanks.tank_.angle = 0
    elif input_k(leha.K_s):
        if tanks.tank_.inWindowDown():
            move_vec[1] -= 2
        tanks.tank_.angle = 180
    elif input_k(leha.K_a):
        if tanks.tank_.inWindowLeft():
            move_vec[0] -= 2
        tanks.tank_.angle = 90
    elif input_k(leha.K_d):
        if tanks.tank_.inWindowRight():
            move_vec[0] += 2
        tanks.tank_.angle = 270
    if input_k(leha.K_SPACE):
        current_time = leha.time.get_ticks()
        if current_time >= speed_shoot:
            speed_shoot = leha.time.get_ticks() + 1000
            create_bull(tanks)

    for b in tanks.bullets:
        if b.pos[0] != spawn_pos and b.pos[1] != spawn_pos:
            gobj = b.collision()
            if gobj and gobj.type_ == 'Wall':
                crt_anim_vz(tanks, gobj.pos[0], gobj.pos[1])
                tanks.win.list_objects.remove(gobj)
                tanks.win.list_objects.remove(b)
                tanks.bullets.remove(b)
            elif gobj and gobj.type_ == 'ProtWall':
                crt_anim_vz(tanks, b.pos[0], b.pos[1])
                tanks.win.list_objects.remove(b)
                tanks.bullets.remove(b)
            elif gobj and gobj.type_ == 'Enemy':
                enem = find_enemy_of_game_obj(tanks, gobj)
                enem.health -= damage
                if enem.check_hp():
                    crt_anim_vz(tanks, b.pos[0], b.pos[1])
                else:
                    crt_anim_vz(tanks, gobj.pos[0], gobj.pos[1])
                tanks.win.list_objects.remove(b)
                tanks.bullets.remove(b)
            elif b.pos[0] < 0 or b.pos[1] < 50 or b.pos[0] > tanks.win.width_win or b.pos[1] > tanks.win.height_win:
                tanks.win.list_objects.remove(b)
                tanks.bullets.remove(b)

    for enm in tanks.list_enemy:
        enm.move_()

    if not tanks.tank_.collision():
        tanks.pos_tp = [tanks.tank_.pos[0], tanks.tank_.pos[1]]
        tanks.tank_.move(move_vec, 1)
    elif move_vec != tanks.old_vec:
        tanks.tank_.set_position(tanks.pos_tp)

    tanks.old_vec = move_vec


spawn_pos = -9999
damage = 10
speed_shoot = 1000
