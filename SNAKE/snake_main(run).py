from framework_LehaEngine import *
import random


def move():
    global move_vec
    if input_k(leha.K_w):
        move_vec = [0, -speed]
    elif input_k(leha.K_s):
        move_vec = [0, speed]
    elif input_k(leha.K_a):
        move_vec = [-speed, 0]
    elif input_k(leha.K_d):
        move_vec = [speed, 0]
    curr_pos[0] += move_vec[0]
    curr_pos[1] += move_vec[1]


def update_apple():
    apple.pos = [random.randrange(width_len) * speed, random.randrange(height_len) * speed]


def check_apple():
    if apple.pos == curr_pos:
        update_apple()
        return False
    return True


win = Window([0, 0], "SNAKE", full_sc=True)
head_copy, head = win.find_object_of_name("snake_head_deb"), win.find_object_of_name("snake_head")
comp = head.components
list_heads = [head]
speed = head_copy.size[0]
time = 100
end_time = time
curr_pos = head_copy.pos
width_len, height_len = 1707 // speed, 1067 // speed
apple = win.find_object_of_name("apple")
update_apple()
move_vec = [0, 0]

while check_run():
    win.fill_window(), win.update_game_objects()
    if get_current_time() >= end_time:
        end_time += time
        move()
        dl = check_apple()
        list_heads.insert(0, win.copy(head_copy, pos=curr_pos, components=comp))
        if dl:
            win.destroy_game_object(list_heads[-1])
            list_heads.pop(-1)
    set_caption("fps:" + str(round(win.get_fps(), 2))), win.update_window()
quit_app()
