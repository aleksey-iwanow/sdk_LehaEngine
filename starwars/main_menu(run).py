from framework_LehaEngine import *
import random


def check_shoot(obj):
    coll = obj.collision()
    if coll and coll.type_ == 'Asteroid':
        obj.pos = [9999, 9999]
        coll.type_ = 'None'
        for a in asteroids:
            if a[0].name == coll.name:
                a[3] = False


def start_game():
    global is_start_game
    is_start_game = True
    but_play.activeself = False


def move_():
    if is_start_game:
        move_vec = [0, 0]
        if input_k(leha.K_w):
            move_vec[1] += 4
        elif input_k(leha.K_s):
            move_vec[1] -= 4
        if input_k(leha.K_a):
            move_vec[0] -= 6
        elif input_k(leha.K_d):
            move_vec[0] += 6
        ship.move(move_vec, 1)


def draw():
    global shoot_time, num1, score
    current_time = leha.time.get_ticks()
    if len(asteroids) < col_ast:
        for num in range(col_ast):
            name_ = ast_copy.name + str(num)
            for ast in asteroids:
                if int(ast[0].name[len(ast_copy.name):]) == num:
                    name_ = ''
            if name_:
                asteroids.append([win.create_object(name_, ast_copy.path, [random.randint(0, win.width_win), -200], [random.randint(60, 100), random.randint(60, 100)], is_collision=ast_copy.is_collision, components=ast_copy.components), random.randint(1, 5000), False, True])
                break
    for a in asteroids:
        if not a[3]:
            if a[0].Animation:
                a[0].size = [130, 130]
                a[0].find_animation('vzriv').active = True
                a[0].Rigidbody.active = False
                score += 1
                value.Text.set_text(f'Score:{score}')
                asteroids.remove(a)
        else:
            if a[0].pos[1] >= win.height_win + a[0].size[1] / 2 or not a[2]:
                a[0].pos = [random.randint(0, win.width_win), -200]

            if current_time >= a[1] and not a[2]:
                a[1] = leha.time.get_ticks() + a[1]
                a[2] = True
    i = 0
    for j in range(0, len(bullets) // 2):
        if i + 1 < len(bullets):
            b = bullets[i]
            b2 = bullets[i + 1]
            bulls_copy = [b, b2]
            for bul in bulls_copy:
                if bul[0].pos[1] < -(bul[0].size[1] / 2):
                    for bb in bulls_copy:
                        if bb[0] in win.list_objects:
                            win.destroy_game_object(bb[0])
                            bullets.remove(bb)
                            continue
        i += 2
    while len(bullets) > 12:
        win.destroy_game_object(bullets[0][0])
        bullets.remove(bullets[0])
    if current_time >= shoot_time and input_k(leha.K_SPACE):
        shoot_time = current_time + speed_shoot
        bullets.append([win.copy(bul1), True])
        bullets.append([win.copy(bul2), True])
        bullets[-2][0].pos, bullets[-1][0].pos = [-37 + ship.pos[0], -44 + ship.pos[1]], [37 + ship.pos[0], -44 + ship.pos[1]]


win = Window([1000, 600], "starwars", (0, 0), 100)
ship = win.find_object_of_name('ship')
but_play = win.find_object_of_name('button_play')
bul1, bul2 = win.find_object_of_name('bullet'), win.find_object_of_name('bullet_1')
bul1.activeself, bul2.activeself = False, False
is_start_game = False
value = win.find_object_of_name("value_ui")
bullets = [[win.copy(bul1), True], [win.copy(bul2), True]]
old_pos = [x[0].pos for x in bullets]
col_ast = 10
score = 0
speed_shoot = 500
shoot_time = speed_shoot
ast_copy = win.find_object_of_name('asteroid')
asteroids = [[win.create_object(ast_copy.name + str(x), ast_copy.path, [random.randint(0, win.width_win), -200], [random.randint(60, 100), random.randint(60, 100)], is_collision=ast_copy.is_collision, components=ast_copy.components), random.randint(1, 5000), False, True] for x in range(col_ast)]

while check_run():
    win.fill_window()
    draw()
    win.update_game_objects()
    set_caption(f'fps: {str(round(win.get_fps(), 2))}')
    win.update_window()
quit_app()
