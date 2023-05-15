import math

from framework_LehaEngine import *


class Bullet:
    def __init__(self):
        pass


def rotate_(gameObj):
    xPos, yPos = leha.mouse.get_pos()
    vectorX = xPos - (gameObj.pos[0] + gameObj.parent.pos[0])
    vectorY = yPos - (gameObj.pos[1] + gameObj.parent.pos[1])
    ang = math.atan2(vectorY, vectorX)
    ang = (180 / math.pi) * (ang if gameObj.flip_sprite_x else - ang)
    gameObj.angle = ang + (0 if gameObj.flip_sprite_x else 180)


def move_():
    global pos_tp
    global old_vec

    move_vec = [0, 0]

    if input_k(leha.K_w):
        move_vec[1] -= 6
    elif input_k(leha.K_s):
        move_vec[1] += 6
    if input_k(leha.K_a):
        move_vec[0] += 6
        gameObject1.flip_sprite_x = False
        ak_47.flip_sprite_x = False
        ak_47.pos[0] = -95
    elif input_k(leha.K_d):
        move_vec[0] -= 6
        gameObject1.flip_sprite_x = True
        ak_47.flip_sprite_x = True
        ak_47.pos[0] = 95
    if input_k(leha.BUTTON_LEFT):
        print('shoot')
        # bullet = win.create_object('bullet', )

    camera.move(move_vec, 1)


win = Window([1000, 600], "project_stethem", (0, 0), 100)
camera = win.camera
pos_tp = []
gameObject1 = win.find_object_of_name('game')
win.add_object_in_camera(gameObject1)
ak_47 = win.find_object_of_name('ak_47')
ak_47.parent = gameObject1
ak_47.pos = [-95, 42]
old_vec = []
bullets = []

while check_run():
    win.fill_window()
    win.update_game_objects()
    set_caption(f'fps: {str(round(win.get_fps(), 2))}')
    win.update_window()

quit_app()
