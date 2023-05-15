import os
import random
import pygame as leha
import importlib
from inspect import isfunction, getsource


FPS_LS = []
PROJECT = ''


def booled(arg):
    if not arg or str(arg).lower().strip() == 'false' or str(arg).lower().strip() == 'none':
        return False
    else:
        return True


class GameObject:
    def __init__(self, window, name, image_path, pos, size, angle, opacity, is_collision=False, add_to_list=True, components="", parent=None):
        self.name = name
        self.window = window
        self.path = image_path
        self.globalPos = pos
        self.rectpos = pos

        self.size = size
        self.angle = angle
        self.activeself = True
        self.collide = False
        self.is_collision = is_collision
        self.old_pos = pos
        self.old_vector_moving = [0, 0]
        self.components = components
        self.Animation = []
        self.Rigidbody = None
        self.AudioSource = []
        self.ColorBox = None
        self.Text = None
        self.argument = None
        self.UI = None
        self.Button = None
        self.Collider = None
        self.ParticleSystem = None
        self.opacity = opacity
        self.type_ = "Default"
        self.parent = parent
        if self.parent:
            self.pos = [self.globalPos[0] - self.parent.globalPos[0], self.globalPos[1] - self.parent.globalPos[1]]
        else:
            self.pos = self.globalPos
        self.image = None
        self.sprite_copy = None
        self.rect = None
        if self.path != 'None':
            self.set_image(leha.image.load(self.window.path_delta + self.path if self.window.b else self.path))

        self.flip_sprite_x = False
        self.flip_sprite_y = False
        self.audio = None
        self.end_time = 0

        self.add_to_list = add_to_list

    def set_parent(self, parent):
        self.parent = parent
        if self.parent:
            self.pos = [self.globalPos[0] - self.parent.globalPos[0], self.globalPos[1] - self.parent.globalPos[1]]
        else:
            self.pos = self.globalPos

    def find_source(self, type_):
        for s in self.AudioSource:
            if s.type_ == type_:
                return s
        return None

    def set_image(self, img):
        self.image = img
        self.image.set_alpha(255 * self.opacity)
        self.image = leha.transform.scale(self.image, (self.size[0], self.size[1]))
        self.image = leha.transform.rotate(self.image, self.angle)
        self.sprite_copy = self.image
        self.rect = self.image.get_rect(center=(self.rect.center[0] if self.rect else self.globalPos[0], self.rect.center[1] if self.rect else self.globalPos[1]))

    def set_opacity(self, opacity):
        self.opacity = opacity
        self.image.set_alpha(255 * self.opacity)
        self.sprite_copy = self.image

    def draw(self, win):
        if self.ParticleSystem:
            self.ParticleSystem.check_time()
            for i in self.ParticleSystem.particles:
                i.move_()
                i.draw(win)
        if self.activeself:
            if self.Rigidbody:
                self.update_rigidbody()
            if self.path != 'None' and not self.ColorBox:
                self.image = leha.transform.scale(self.sprite_copy, (self.size[0] * self.window.scale_factor, self.size[1] * self.window.scale_factor))
                image2 = leha.transform.rotate(self.image, self.angle)
                r = image2.get_rect(center=(self.rect.center[0], self.rect.center[1]))
                self.image = image2
                self.image = leha.transform.flip(self.image, self.flip_sprite_x, self.flip_sprite_y)
                win.blit(self.image, r)
            elif self.ColorBox:
                cl = self.ColorBox.color_rgb
                s = leha.Surface((self.size[0], self.size[1]), leha.SRCALPHA)
                s.fill((cl[0], cl[1], cl[2], int(255 * self.opacity)))
                win.blit(s, (self.rectpos[0] - self.size[0] // 2, self.rectpos[1] - self.size[1] // 2))
            if self.Text:
                if self.Text.is_center:
                    text_rect = self.Text.text_render.get_rect(center=(self.rectpos[0], self.rectpos[1]))
                    win.blit(self.Text.text_render, text_rect)
                else:
                    win.blit(self.Text.text_render, (self.rectpos[0] - self.size[0] / 2 + self.Text.pad[0], self.rectpos[1] - self.size[1] / 2 + self.Text.pad[1]))

    def move(self, vector, speed, power=1, is_time=True, type_exceptions=None, not_collision=None):
        current_time = leha.time.get_ticks()
        if current_time >= self.end_time or not is_time:
            self.end_time = leha.time.get_ticks() + speed
            vec = leha.Vector2((vector[0], -vector[1]))
            vc = (vec * power)
            if self.name == 'camera-main':
                for p in self.window.list_objects_in_camera:
                    if not_collision or ((p.Collider or p.rect) and not p.collision(vc=[-vc[0], -vc[1]], type_exceptions=type_exceptions)):
                        self.pos += vc
            else:
                if not_collision or ((self.Collider or self.rect) and not self.collision(vc=[vc[0], vc[1]], type_exceptions=type_exceptions)):
                    self.pos += vc

    def update_anim(self):
        current_tm = leha.time.get_ticks()
        for an in self.Animation:
            if current_tm >= an.end_time and len(an.frames) > an.sprite_index and an.active:
                an.end_time = leha.time.get_ticks() + an.time
                self.image = leha.transform.scale(an.frames[an.sprite_index], (self.size[0], self.size[1]))
                self.sprite_copy = self.image
                an.sprite_index += 1
                if an.sprite_index == len(an.frames):
                    if an.looping:
                        an.sprite_index = 0
                    if an.is_deleted:
                        self.window.destroy_game_object(self)

    def set_position(self, p):
        self.pos = list(p)

    def find_animation(self, tag):
        for animation in self.Animation:
            if animation.tag == tag:
                return animation
        return None

    def setType(self, tp):
        self.type_ = tp

    def inWindowLeft(self, pad=0):
        if self.rect.x <= 0:
            return False
        return True

    def inWindowRight(self, pad=0):
        if self.rect.x + self.rect.width >= self.window.width_win:
            return False
        return True

    def inWindowUp(self, pad=0):
        if self.rect.y <= pad:
            return False
        return True

    def inWindowDown(self, pad=0):
        if self.rect.y + self.rect.height >= self.window.height_win:
            return False
        return True

    def inWindow(self):
        if self.rect.y >= self.window.height_win or self.rect.y + self.rect.height <= 0 or self.rect.x >= self.window.width_win or self.rect.x + self.rect.width <= 0:
            return False
        return True

    def collision(self, vc=None, type_exceptions=None):
        xv = vc[0] if vc else 0
        yv = vc[1] if vc else 0
        objs = self.window.get_collision_objects()
        for o in objs:
            if o.Collider:
                rc = leha.Rect((o.rect.x + o.Collider.x) + o.size[0] // 2, (o.rect.y + o.Collider.y) + o.size[0] // 2, o.Collider.w, o.Collider.h)
                rc.center = ((o.rect.x + o.Collider.x) + o.size[0] // 2, (o.rect.y + o.Collider.y) + o.size[0] // 2)
            else:
                rc = o.rect

            b = rc.colliderect(leha.Rect(self.Collider.rect.x + xv, self.Collider.rect.y + yv, self.Collider.rect.width, self.Collider.rect.height) if self.Collider else leha.Rect(self.rect.x + xv, self.rect.y + yv, self.rect.width, self.rect.height))
            if o.name != self.name and b and (not type_exceptions or (type_exceptions and o.type_ != type_exceptions)):
                return o
        return None

    def set_animation(self, frames, looping, time, active, is_deleted):
        self.Animation = Animation(frames, time, looping, active, is_deleted)

    def update_rigidbody(self):
        if self.Rigidbody.active:
            if self.Rigidbody.gravity:
                self.pos = [self.pos[0], self.pos[1] + self.Rigidbody.power]
            else:
                self.pos = [self.pos[0], self.pos[1] - self.Rigidbody.power]


class Animation:
    def __init__(self, frames, time, is_looping, active, is_deleted, tag):
        self.frames = frames
        self.time = time
        self.looping = is_looping
        self.active = active
        self.is_deleted = is_deleted
        self.tag = tag
        self.sprite_index = 0
        self.end_time = 0


class Rigidbody:
    def __init__(self, gravity, power, active):
        self.power = power
        self.gravity = gravity
        self.active = active


class ColorBox:
    def __init__(self, color):
        self.color = color
        if color != 'None':
            self.color_rgb = leha.Color(color)
        else:
            self.color_rgb = (255, 255, 255)

    def set_color(self, color):
        if color != 'None':
            self.color_rgb = leha.Color(color)
        else:
            self.color_rgb = (255, 255, 255)


class UIG:
    def __init__(self, active):
        self.active = active


class Text:
    def __init__(self, text, sizef, colorf):
        self.text = text
        self.sizef = sizef
        self.colorf = colorf
        self.cl2 = leha.Color(self.colorf)
        self.font = leha.font.SysFont('Comic Sans MS', self.sizef)
        self.text_render = self.font.render(self.text, True, self.cl2)

        self.is_center = True
        self.pad = [10, 10]

    def set_text(self, text):
        self.text = text
        self.text_render = self.font.render(self.text, True, self.cl2)

    def set_color(self, color):
        self.cl2 = leha.Color(color)
        self.text_render = self.font.render(self.text, True, self.cl2)


class Collider:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = leha.rect.Rect(x, y, w, h)


class Button:
    def __init__(self, function, color_click, color_loc, gm):
        self.gameObject = gm
        self.start_color = None
        if self.gameObject.ColorBox:
            self.start_color = self.gameObject.ColorBox.color_rgb
        self.function = function
        self.func_ = None
        self.color_click = color_click
        self.color_loc = color_loc
        self.time_cl = 500
        self.delta_time = self.time_cl

    def set_func(self, func):
        self.func_ = func

    def click(self):
        if self.start_color:
            self.gameObject.ColorBox.color_rgb = self.start_color

        rect = leha.Rect((self.gameObject.rectpos[0] - self.gameObject.size[0] // 2, self.gameObject.rectpos[1] - self.gameObject.size[1] // 2, self.gameObject.size[0], self.gameObject.size[1]))
        if rect.collidepoint(leha.mouse.get_pos()[0], leha.mouse.get_pos()[1]):
            if self.color_loc != 'None' and self.start_color:
                cl = self.gameObject.ColorBox.color_rgb
                self.gameObject.ColorBox.color_rgb = ((cl[0] - 15) if cl[0] >= 10 else 0, (cl[1] - 15) if cl[1] >= 15 else 0, (cl[2] - 15) if cl[2] >= 15 else 0)
            if leha.mouse.get_pressed()[0] and get_current_time() >= self.delta_time:
                self.delta_time = get_current_time() + self.time_cl
                if self.gameObject.ColorBox:
                    cl = self.gameObject.ColorBox.color_rgb
                    self.gameObject.ColorBox.color_rgb = (
                    (cl[0] - 30) if cl[0] >= 30 else 0, (cl[1] - 30) if cl[1] >= 30 else 0,
                    (cl[2] - 30) if cl[2] >= 30 else 0)
                if self.func_:
                    self.func_()
                else:
                    eval(self.function)


class Particle:
    def __init__(self, p, position, gm):
        self.p = p
        self.position = [0, 0]
        self.rect_position = [position[0], position[1]]
        self.start_position = [position[0], position[1]]
        numbers = range(-5, 6)
        self.dx = random.choice(numbers)
        self.dy = random.choice(numbers)
        while not self.dx and not self.dy:
            self.dx = random.choice(numbers)
            self.dy = random.choice(numbers)
        self.gm = gm
        self.delta_time = 0
        self.opacity = 1

    def draw(self, win):
        win.blit(self.gm, (round(self.rect_position[0] * self.p.gameObject.window.scale_factor), round(self.rect_position[1] * self.p.gameObject.window.scale_factor)))

    def set_opacity(self, op):
        self.opacity = op
        if self.opacity <= 0:
            self.p.particles.remove(self)
        else:
            self.gm.set_alpha(255 * self.opacity)

    def move_(self, time=10):
        if get_current_time() > self.delta_time:
            self.delta_time = get_current_time() + time
            self.position[0] += self.dx
            self.position[1] += self.dy
            self.rect_position[0] = self.position[0] + self.p.gameObject.rectpos[0]
            self.rect_position[1] = self.position[1] + self.p.gameObject.rectpos[1]


class Particles:
    def __init__(self, gameObject, active, looping, count, time):
        self.count = count
        self.active = active
        self.looping = looping
        self.time = time + get_current_time()
        self.gameObject = gameObject
        self.particles = []
        self.img = self.gameObject.sprite_copy
        self.time_destroy = 20
        self.delta_destroy = self.time_destroy
        self.set_particle()
        self.is_destroy = False

    def check_time(self):
        cur = get_current_time()
        if not self.particles:
            gm = self.gameObject
            self.gameObject.window.list_objects.remove(gm)
        if cur > self.time and not self.is_destroy:
            self.is_destroy = True
        if cur > self.delta_destroy and self.is_destroy:
            self.delta_destroy = cur + self.time_destroy
            for i in self.particles:
                i.set_opacity(i.opacity - 0.1)

    def set_particle(self):
        for i in range(self.count):
            self.particles.append(Particle(self, [self.gameObject.rectpos[0], self.gameObject.rectpos[1]], self.img))


class AudioSource:
    def __init__(self, sound_track, volume, active, looping, type_):
        self.sound_track = sound_track
        self.active = active
        self.looping = looping
        self.type_ = type_
        self.audio = leha.mixer.Sound(self.sound_track)
        self.is_playing = False
        self.volume = volume
        self.audio.set_volume(self.volume)
        if self.active:
            self.play()

    def play(self):
        if not self.looping:
            self.audio.play()
        else:
            self.is_playing = True
            self.audio.play(-1)

    def stop(self):
        self.audio.stop()
        self.is_playing = False


class Window:
    def __init__(self, size, filepath="", pos_camera=(0, 0), fps=100, full_sc=False, scenes=None):
        leha.init()
        leha.font.init()
        global PROJECT
        PROJECT = os.getcwd()
        filepath = PROJECT
        if not scenes:
            filepath = filepath + '\\' + [f for f in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, f)) and len(f.split('.')) > 1 and f.split('.')[-1] == 'scenes'][0]
        self.width_win = size[0]
        self.height_win = size[1]
        if full_sc:
            self.window = leha.display.set_mode((0, 0), leha.FULLSCREEN)
        else:
            self.window = leha.display.set_mode((self.width_win, self.height_win))
        self.clock_ = leha.time.Clock()
        self.FPS = fps

        self.camera = GameObject(self, 'camera-main', 'None', pos_camera, 1, [0, 0], 0)
        self.scale_factor = 1
        self.list_objects = []
        self.list_debug_objects = []
        self.list_anim = []
        self.list_objects_in_camera = []
        self.isStart = True
        self.scenes = []
        self.index_scene_now = 0

        self.upd_sec = leha.time.get_ticks() + 100

        pathcwd = os.getcwd()
        self.b = True if pathcwd.split('\\')[-1] != filepath.split('\\')[-2] else False
        filepath = filepath if self.b else filepath.split('\\')[-1]

        self.path_delta = filepath[:-len(filepath.split('\\')[-1])]

        with open(f'{pathcwd}\\{filepath}') as fl:
            for i in fl.read().split('\n'):
                if self.b:
                    self.scenes.append(self.path_delta + i)
                else:
                    self.scenes.append(i)

        self.fl_now = self.scenes[0]
        # открываем файл сцены
        self.load_scene(self.fl_now)

    def set_scene(self, index):
        self.index_scene_now = index
        self.fl_now = self.scenes[index]
        self.load_scene(self.fl_now)

    def copy(self, gameObject, pos=None, components=None, index=None):
        return self.create_object(gameObject.name, gameObject.path, [pos[0], pos[1]] if pos else gameObject.pos, gameObject.size, gameObject.angle, gameObject.opacity, gameObject.is_collision, gameObject.add_to_list, components if components else gameObject.components, index if index else (self.list_objects.index(gameObject) + 1))

    def get_objects_from_scene(self, index):
        list_objects, list_debug_objects, list_ui = [], [], []
        with open(self.scenes[index], 'r') as fl:
            rd = fl.read()
            split_ = rd.split('(~&~)')
            sp1 = split_[0].split('~')
            if rd.strip('\n') != '':
                if split_[0].strip('\n') != '':
                    for i in sp1:
                        objparam = i.split('\n')
                        gm = GameObject(self,
                                        objparam[0],
                                        objparam[1],
                                        [int(a) for a in objparam[2].split(',')],
                                        [int(a) for a in objparam[3].split(',')],
                                        int(objparam[4]),
                                        float(objparam[5]),
                                        booled(eval(objparam[6])),
                                        booled(eval(objparam[7])),
                                        objparam[8] if len(objparam) > 9 else "",
                                        self.find_object_of_name(objparam[9]) if len(objparam) > 9 else self.find_object_of_name(objparam[9]))
                        # добавляем gameObject из файлаfind_objects_of_parameter
                        if gm.add_to_list:
                            list_objects.append(gm)
                        else:
                            list_debug_objects.append(gm)
        return [list_objects, list_debug_objects]

    def load_scene(self, file_):
        self.list_objects.clear()
        self.list_debug_objects.clear()
        self.list_anim.clear()
        self.list_objects_in_camera.clear()

        with open(file_, 'r') as fl:
            rd = fl.read()
            split_ = rd.split('(~&~)')
            sp1 = split_[0].split('~')
            if rd.strip() != '':
                if split_[0].strip() != '':
                    for i in sp1:
                        objparam = i.split('\n')
                        objparam = [a for a in objparam if a]
                        gm = GameObject(self,
                                        objparam[0],
                                        objparam[1],
                                        [int(a) for a in objparam[2].split(',')],
                                        [int(a) for a in objparam[3].split(',')],
                                        int(objparam[4]),
                                        float(objparam[5]),
                                        booled(eval(objparam[6])),
                                        booled(eval(objparam[7])),
                                        objparam[8] if len(objparam) > 9 else "")
                        # добавляем gameObject из файла
                        if gm.add_to_list:
                            self.list_objects.append(gm)
                        else:
                            self.list_debug_objects.append(gm)
        self.isStart = True

    def update_window(self):
        self.isStart = False
        if self.upd_sec <= leha.time.get_ticks():
            self.upd_sec = leha.time.get_ticks() + 100
            FPS_LS.append(self.clock_.get_fps())
        leha.display.flip()

    def fill_window(self, color_=(0, 0, 0)):
        self.clock_.tick(self.FPS)
        self.window.fill(color_)

    def get_fps(self):
        return self.clock_.get_fps()

    def update_all(self):
        self.fill_window((0, 0, 0))
        self.update_game_objects()
        self.update_window()

    def get_collision_objects(self):
        coll_obj = []
        for obj in self.list_objects:
            if obj.is_collision and obj.inWindow():
                coll_obj.append(obj)
        return coll_obj

    def destroy_game_object(self, object_):
        try:
            self.list_objects.remove(object_)
        except ValueError:
            print('ValueError')

    def add_object_in_camera(self, object_):
        self.list_objects_in_camera.append(object_)

    def update_game_objects(engine):
        for gameObject in engine.list_objects:
            if gameObject.name != 'anim_':
                try:
                    if gameObject not in engine.list_objects_in_camera and (not gameObject.UI or (gameObject.UI and not gameObject.UI.active)):
                        gameObject.rectpos = [(gameObject.pos[0] + engine.camera.pos[0]) * engine.scale_factor, (gameObject.pos[1] + engine.camera.pos[1]) * engine.scale_factor]
                        gameObject.rect.center = gameObject.rectpos
                    if gameObject.parent:
                        gameObject.rectpos = [(gameObject.pos[0] + gameObject.parent.pos[0]) * engine.scale_factor, (gameObject.pos[1] + gameObject.parent.pos[1]) * engine.scale_factor]
                        gameObject.rect.center = gameObject.rectpos

                except AttributeError:
                    pass
                for c in gameObject.components.split('$'):
                    if c:
                        cps = c.split('^,^')
                        c2 = cps[2].split("^;^")
                        if cps[0] == "Function":
                            if booled(c2[0].strip()) or (not booled(c2[0].strip()) and engine.isStart):
                                exec(f'{c2[1]}')
                        elif cps[0] == 'Audio source':
                            if engine.isStart:
                                gameObject.AudioSource.append(AudioSource(engine.path_delta + c2[0], float(c2[1]), booled(c2[2]), booled(c2[3]), c2[4]))
                        elif cps[0] == "Color box":
                            if not gameObject.ColorBox:
                                gameObject.ColorBox = ColorBox(c2[0])
                        elif cps[0] == 'Text':
                            if not gameObject.Text:
                                gameObject.Text = Text(c2[0], int(c2[1]), c2[2])
                        elif cps[0] == 'Button':
                            if not gameObject.Button:
                                gameObject.Button = Button(c2[0], c2[1], c2[2], gameObject)
                        elif cps[0] == 'UI':
                            if not gameObject.UI:
                                gameObject.UI = UIG(booled(c2[0]))
                        elif cps[0] == 'Particle system':
                            if not gameObject.ParticleSystem:
                                gameObject.ParticleSystem = Particles(gameObject, booled(c2[0]), booled(c2[1]), int(c2[2]), int(c2[3]))
                        elif cps[0] == 'Activeself':
                            if engine.isStart:
                                gameObject.activeself = booled(c2[0])
                        elif cps[0] == 'Collider':
                            if not gameObject.Collider:
                                gameObject.Collider = Collider(int(c2[0]), int(c2[1]), int(c2[2]), int(c2[3]))
                        elif cps[0] == "Rigidbody":
                            if not gameObject.Rigidbody:
                                gameObject.Rigidbody = Rigidbody(booled(c2[0]), int(c2[1]), booled(c2[2]))
                        elif cps[0] == "Script":
                            if c2[0].strip() == "True" or (c2[0].strip() == "False" and engine.isStart):
                                os.system(f'python {c2[1]}')
                        elif cps[0] == "Animation":
                            if engine.isStart:
                                frames = c2[1].split('*&*')
                                f = []
                                for p in frames:
                                    image = leha.image.load(engine.path_delta + p if engine.b else p)
                                    image.set_alpha(255 * gameObject.opacity)
                                    image = leha.transform.rotate(image, gameObject.angle)
                                    f.append(image)
                                gameObject.Animation.append(Animation(f, int(c2[3]), booled(c2[2]), booled(c2[4]), booled(c2[5]), c2[6]))
                if gameObject.Animation:
                    gameObject.update_anim()
                if (gameObject.rect and gameObject.inWindow()) or gameObject.ColorBox or gameObject.Text:
                    gameObject.draw(engine.window)
                    if gameObject.Button:
                        gameObject.Button.click()

        for gameObject in engine.list_debug_objects:
            for c in gameObject.components.split('$'):
                if c:
                    cps = c.split('^,^')
                    if cps[0] == "Function":
                        c2 = cps[2].split("^;^")
                        if c2[0].strip() == "True" or (c2[0].strip() == "False" and engine.isStart):
                            exec(f'{c2[1]}')
                    elif cps[0] == "Script":
                        if cps[1] == "update" or (cps[1] == "start" and engine.isStart):
                            os.system(f'python {cps[2]}')

    def delete_anim(self, anim):
        self.list_anim.remove(anim)

    def find_object_of_name(self, name_):
        obj = self.find_objects_of_parameter(name_, 'name')
        try:
            return obj[0]
        except IndexError:
            pass

    def find_ui_of_name(self, name_):
        obj = self.find_ui_objects_of_parameter(name_, 'name')
        return obj[0]

    def create_animation(self, frames, pos, size, time, looping, active=True, is_deleted = False, index=-1, name='AnimationTest', angle=0, opacity=1, is_collision=False):
        gmObj = GameObject(self, name, frames[0], pos, size, angle, opacity, is_collision, True)
        f = []
        for p in frames:
            image = leha.image.load(self.path_delta + p if self.b else p)
            image.set_alpha(255 * opacity)
            image = leha.transform.scale(image, (size[0], size[1]))
            image = leha.transform.rotate(image, angle)
            f.append(image)
        gmObj.set_animation(f, looping, time, active, is_deleted)
        self.list_objects.insert(index, gmObj)

    def get_index(self, game_obj):
        return self.list_objects.index(game_obj)

    def find_objects_of_parameter(self, par_, type_):
        objs = []
        isSplit = False
        if type(par_) == str:
            par_ = par_.split('||')
            isSplit = True
        for ob in self.list_objects:
            if isSplit:
                for p in par_:
                    if eval('ob.' + type_) == p:
                        objs.append(ob)
            else:
                if eval('ob.' + type_) == par_:
                    objs.append(ob)
        return objs

    def vector_of(self, gm1, gm2):
        k = gm2.pos[0] - gm1.pos[0]
        k2 = gm2.pos[1] - gm1.pos[1]

        if k2 > k:
            ln = len(str(k2))
        else:
            ln = len(str(k))
        ln = 10 ** (ln - 1)
        return [k / ln, k2 / ln]

    def find_debug_objects_of_parameter(self, par_, type_):
        objs = []
        ls = self.list_debug_objects
        for ob in ls:
            lr = eval('ob.' + type_)
            if lr == par_:
                objs.append(ob)
        return objs

    def find_ui_objects_of_parameter(self, par_, type_):
        objs = []
        ls = self.list_ui
        for ob in ls:
            lr = eval('ob.' + type_)
            if lr == par_:
                objs.append(ob)
        return objs

    def get_name_recur(self, ls, name_, num=0, nm=''):
        for i in ls:
            nm = name_ if num == 0 else (f'{name_[:-2]}_{num}' if name_[-2] == '_' and name_[-1].isdigit() else f'{name_}_{num}')
            if i.name == nm:
                return self.get_name_recur(ls, name_, num + 1, nm)

        return nm

    def create_object(self, name_, path_image, pos, size, angle=0, opacity=1, is_collision=False, add_to_list=True, components="", indInsert=-1):
        name = self.get_name_recur(self.list_objects, name_,
                                 (int(name_[-1]) if name_[-2] == '_' and name_[-1].isdigit() else 0))
        gm = GameObject(self, name, path_image, pos, size, angle, opacity, is_collision, add_to_list, components)
        self.list_objects.insert(indInsert, gm)

        return gm

    def set_index(self, gameObject, index):
        self.list_objects.remove(gameObject)
        self.list_objects.insert(index, gameObject)


def run_function_from_code(code, func, *argv):
    module = importlib.import_module(code)
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isfunction(attribute) and attribute_name == func:
            attribute(*argv)


def input_k(key_pygame):
    keys = leha.key.get_pressed()
    if keys[key_pygame]:
        return True
    return False


def event_check(ev):
    for event in leha.event.get():
        if event.type == ev:
            return event
    return False


def check_run():
    for event in leha.event.get():
        if event.type == leha.QUIT:
            return False
    return True


def quit_app():
    with open(f'{PROJECT}/fps.settings', 'w') as fl:
        for i in FPS_LS:
            fl.write(str(round(i)) + '\n')
    os.chdir('C:\\Users\\aleks\\PycharmProjects\\sdk___')
    leha.quit()


def get_current_time():
    return leha.time.get_ticks()


def get_mouse_pos():
    return leha.mouse.get_pos()


def set_caption(text):
    leha.display.set_caption(text)


FUNCTIONS = {'run_function_from_code': run_function_from_code,
             'input_k': input_k,
             'check_run': check_run,
             'quit_app': quit_app,
             'set_caption': set_caption}
