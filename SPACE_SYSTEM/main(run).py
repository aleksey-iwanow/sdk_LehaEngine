import math
from framework_LehaEngine import *


def update_planet(radius, planet, current_angle, pos_center, rp, is_satellite=False):
    n_rad = current_angle * math.pi / 180
    x0, y0 = pos_center[0] + radius * math.cos(n_rad), pos_center[1] + radius * math.sin(n_rad)
    current_angle += float(planet.argument[0])
    if is_satellite:
        planet.rectpos = [x0, y0]
    else:
        planet.pos = [x0, y0]
    '''if planet.angle >= 360:
        planet.angle = 0
    else:
        planet.angle += 1'''
    leha.draw.circle(win.window, (240, 240, 240), rp, radius * win.scale_factor, 2)
    return current_angle


def active_panel(gameObject):
    panel.activeself = True
    tx_name.Text.set_text(f"{gameObject.argument[1][0]}")
    tx_mass.Text.set_text(f"{gameObject.argument[1][1]}")


def set_argument(arg):
    arg[0].argument = [arg[1], arg[2]]


def move_():
    mv = [0, 0]
    event_ = event_check(leha.MOUSEWHEEL)
    if event_:
        yw = event_.y
        if yw == 1:
            win.scale_factor += 0.02
        elif yw == -1:
            win.scale_factor -= 0.02
        tx_scale.Text.set_text(f"scale<{round(win.scale_factor, 2)}>")
    if input_k(leha.K_w):
        mv[1] -= 4 / win.scale_factor
    elif input_k(leha.K_s):
        mv[1] += 4 / win.scale_factor
    if input_k(leha.K_a):
        mv[0] += 4 / win.scale_factor
    elif input_k(leha.K_d):
        mv[0] -= 4 / win.scale_factor
    camera.move(mv, 1)


def update_():
    global planets

    for p in planets:
        p[2] = update_planet(p[1], p[0], p[2], [center_x, center_y], star.rectpos)
    satellite[2] = update_planet(satellite[1], satellite[0], satellite[2], planets[3][0].pos, planets[3][0].rectpos)


time_ = 100
current_angle = 0

win = Window([1200, 800], "SPACE_SYSTEM")
camera = win.camera
star = win.find_object_of_name("star")
panel = win.find_object_of_name("panel")
tx_scale = win.find_object_of_name("text_scale")
tx_name = win.find_object_of_name("text_name")
tx_mass = win.find_object_of_name("text_mass")
win.add_object_in_camera(win.find_object_of_name("camera"))
center_x, center_y = star.rectpos[0], star.rectpos[1]

win.update_game_objects()

sll = win.find_object_of_name("satellite")
planets_obj = win.find_objects_of_parameter("planet", "type_")
planets = [[p, ((center_x - p.pos[0]) ** 2 + (center_y - p.pos[1]) ** 2) ** 0.5, 0] for p in planets_obj]
satellite = [sll, 80, 0, planets[3][0].pos]
cur = 0

while check_run():
    cur = get_current_time()
    win.fill_window()
    move_()
    update_()
    win.update_game_objects()
    set_caption("fps:" + str(round(win.get_fps(), 2)))
    win.update_window()

quit_app()
