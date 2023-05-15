from framework_LehaEngine import *


SPEED = 6
SPEED_CONST = SPEED
SPEED_NPC = 5
SPEED_NPC_CONST = SPEED_NPC
RADIUS_MOVE = 500
RADIUS_ATTACK = 65
DAMAGE = 10
HEALTH = 100
TIME_TRADE = 1000
DELTA_TIME_TRADE = TIME_TRADE
TIME_DIALOG = 1000
DELTA_TIME_DIALOG = TIME_DIALOG
LIFE = 1
TRADE = False
INDEX_DIALOG = 0
SCORE = 0
GOLD = 0
MENU = True


class Chest:
    def __init__(self, gm):
        self.gameObject = gm
        self.gold = random.randrange(5, 11)
        self.active_ = True


class Enemy:
    def __init__(self, gm):
        self.gameObject = gm
        self.SPEED_ATTACK = 1000
        self.DELTA_TIME = self.SPEED_ATTACK
        self.TIME_PUSH = 650
        self.DELTA_PUSH = self.TIME_PUSH
        self.SPEED_ATTACK2 = 350
        self.DELTA_TIME2 = self.SPEED_ATTACK2
        self.pushed = False
        self.mv = [0, 0]
        self.HEALTH = 100
        self.MAXHEALTH = self.HEALTH
        self.DAMAGE = 10
        self.old_image = None
        self.hpbar = win.copy(clone_bar)
        self.hpbar2 = win.copy(clone_bar)
        self.k_hp = self.hpbar.size[0] / self.HEALTH
        self.change = True

    def check_hp(self):
        global SCORE, DIALOG, GOLD
        if self.HEALTH <= 0:
            SCORE += 1
            if SCORE == 10:
                DIALOG = DIALOG3
                GOLD += 100
            vz = win.copy(vz_)
            vz.pos = self.gameObject.pos
            win.destroy_game_object(self.hpbar), win.destroy_game_object(self.hpbar2), self.gameObject.find_source('dead').play()
            self.gameObject.find_animation('dead').active = True

    def damage(self):
        self.gameObject.find_source('damage').play()

    def update_bars(self):
        if self.hpbar2.ColorBox and self.change:
            self.change = False
            self.hpbar2.ColorBox.set_color('#5A0F01')
        self.hpbar.pos = [self.gameObject.pos[0] - (round(self.MAXHEALTH * self.k_hp) - round(self.HEALTH * self.k_hp)) // 2, self.gameObject.pos[1] - 45]
        self.hpbar2.pos = [self.gameObject.pos[0], self.gameObject.pos[1] - 45]

    def update_size(self):
        self.hpbar.size = [round(self.HEALTH * self.k_hp), self.hpbar.size[1]]


def chest(object_):
    global GOLD
    if MENU:
        return
    if object_.inWindow():
        animation_attack = sword.find_animation('attack')
        coll = sword.collision()
        if object_.argument and object_.argument.active_ and coll and coll == object_ and animation_attack.active:
            object_.argument.active_ = False
            GOLD += object_.argument.gold
            object_.find_animation('open').active = True
            object_.find_source('open').play()


def add_health():
    global HEALTH, GOLD
    if GOLD >= 10 and HEALTH != 100:
        GOLD -= 10
        HEALTH = 100
        update_bar_player()


def add_damage():
    global DAMAGE, GOLD
    if GOLD >= 20:
        GOLD -= 20
        DAMAGE += 10
        update_bar_player()


def NPC2_trader_update(object_):
    if MENU:
        return
    global DELTA_TIME_TRADE, TRADE, INDEX_DIALOG
    if object_.inWindow():
        coll, an = sword.collision(), sword.find_animation('attack')
        if coll == object_ and not TRADE and an.active and cur >= DELTA_TIME_TRADE:
            INDEX_DIALOG = 0
            back_trade.activeself, avatar_trade.activeself, text_dialog.activeself, TRADE = True, True, True, True
        elif coll == object_ and an and an.active and TRADE and cur >= DELTA_TIME_TRADE:
            DELTA_TIME_TRADE = cur + TIME_TRADE
            if INDEX_DIALOG >= len(DIALOG_TRADE) + 1:
                TRADE, back_trade.activeself, button1.activeself, button2.activeself, hp_txt_tr.activeself, hp_txt_tr_1.activeself, hp_txt_tr_2.activeself, hp_txt_tr_3.activeself, hp_img.activeself, damage_img.activeself = [False for a in range(10)]
                return
            if INDEX_DIALOG < len(DIALOG_TRADE):
                text_dialog.Text.set_text(DIALOG_TRADE[INDEX_DIALOG][0]), avatar_trade.set_image(DIALOG_TRADE[INDEX_DIALOG][1])
            else:
                avatar_trade.activeself, text_dialog.activeself = False, False
                button1.activeself, button2.activeself, hp_txt_tr.activeself, hp_txt_tr_1.activeself, hp_txt_tr_2.activeself, hp_txt_tr_3.activeself, hp_img.activeself, damage_img.activeself = [True for a in range(8)]
            INDEX_DIALOG += 1


def NPC_trader_update(object_):
    if MENU:
        return
    global TRADE, INDEX_DIALOG, DELTA_TIME_DIALOG, DIALOG
    if object_.inWindow():
        an, coll = sword.find_animation('attack'), sword.collision()
        if coll == object_ and not TRADE and an.active and cur >= DELTA_TIME_DIALOG:
            INDEX_DIALOG = 0
            TRADE, back_trade.activeself, avatar_trade.activeself, text_dialog.activeself = True, True, True, True
        elif coll == object_ and an and an.active and TRADE and cur >= DELTA_TIME_DIALOG:
            DELTA_TIME_DIALOG = cur + TIME_DIALOG
            if INDEX_DIALOG >= len(DIALOG):
                if SCORE < 10:
                    DIALOG = DIALOG2
                else:
                    DIALOG = DIALOG4
                TRADE, back_trade.activeself, avatar_trade.activeself, text_dialog.activeself = False, False, False, False
                return
            text_dialog.Text.set_text(DIALOG[INDEX_DIALOG][0]), avatar_trade.set_image(DIALOG[INDEX_DIALOG][1])
            INDEX_DIALOG += 1


def NPC_update(object_):
    if not object_.argument or MENU:
        return
    global HEALTH, LIFE

    x1, y1, x2, y2 = object_.rect.center[0], object_.rect.center[1], player.rect.center[0], player.rect.center[1]
    mov_vec = [0, 0]
    vectorX = x1 - x2
    vectorY = y1 - y2
    length = (((vectorX ** 2) + (vectorY ** 2)) ** 0.5)
    clear_an_sc(object_)
    animation_attack = sword.find_animation('attack')
    if cur >= object_.argument.DELTA_PUSH:
        object_.argument.pushed = False
    if sword.collision() == object_ and animation_attack.active and cur >= object_.argument.DELTA_TIME2:
        object_.argument.HEALTH -= DAMAGE
        object_.argument.damage(), object_.argument.update_size(), object_.argument.check_hp()
        object_.argument.pushed = True
        object_.argument.DELTA_TIME2 = cur + object_.argument.SPEED_ATTACK2
        object_.argument.mv[0], object_.argument.mv[1] = round((vectorX / length) * SPEED_NPC * 2), -round((vectorY / length) * SPEED_NPC * 2)
    if object_.argument.pushed:
        mov_vec[0], mov_vec[1] = object_.argument.mv[0], object_.argument.mv[1]

    elif length > 0:
        object_.argument.DELTA_PUSH = cur + object_.argument.TIME_PUSH
        mov_vec[0], mov_vec[1] = -round((vectorX / length) * SPEED_NPC), round((vectorY / length) * SPEED_NPC)
    if length <= RADIUS_MOVE:
        object_.move(mov_vec, 1, type_exceptions=('enemy' if object_.argument.pushed else None))
        if not object_.argument.pushed:
            object_.flip_sprite_x = False
            if (mov_vec[0] != SPEED_NPC or mov_vec[0] != -SPEED_NPC) and mov_vec[1] < 0:
                object_.find_animation('front').active = True
                object_.argument.old_image = skeleton_1
            elif (mov_vec[0] != SPEED_NPC or mov_vec[0] != -SPEED_NPC) and mov_vec[1] > 0:
                object_.find_animation('rear').active = True
                object_.argument.old_image = skeleton_2
            elif mov_vec[0] == SPEED_NPC:
                object_.flip_sprite_x = False
                object_.find_animation('side').active = True
                object_.argument.old_image = skeleton_3
            elif mov_vec[0] == -SPEED_NPC:
                object_.flip_sprite_x = True
                object_.find_animation('side').active = True
                object_.argument.old_image = skeleton_3

    if object_.argument.old_image and (mov_vec == [0, 0] or length > RADIUS_MOVE):
        object_.set_image(object_.argument.old_image)

    if length < RADIUS_ATTACK and cur >= object_.argument.DELTA_TIME:
        HEALTH -= object_.argument.DAMAGE
        if HEALTH <= 0:
            HEALTH = 100
            LIFE -= 1

        object_.argument.DELTA_TIME = cur + object_.argument.SPEED_ATTACK
        update_bar_player()

    if mov_vec[0] or mov_vec[1]:
        object_.argument.update_bars()


def update_bar_player():
    hp_bar.size[0] = round(HEALTH * k_w)
    hp_bar.rectpos[0] = hp_bar.size[0] // 2


def clear_an():
    for anim in player.Animation:
        anim.active = False


def clear_an_sc(obj):
    for anim in obj.Animation:
        anim.active = False


def set_argument(obj):
    obj.argument = Enemy(obj)


def set_argument_chest(obj):
    obj.argument = Chest(obj)


def check1():
    while sword.pos[1] >= old_del:
        sword.pos[1] -= 50


def check2():
    while sword.pos[1] <= old_del:
        sword.pos[1] += 10


def check3():
    while sword.pos[1] > old_del:
        sword.pos[1] -= 50
    while sword.pos[1] < old_del:
        sword.pos[1] += 10


def play_game():
    global MENU
    MENU = False
    for obj in menu_objects:
        obj.activeself = False


def exit_game():
    quit_app()


def move_():
    if MENU:
        return
    global old_image

    move_vec = [0, 0]
    is_side = True
    clear_an()

    if input_k(leha.K_w) and not TRADE:
        move_vec[1] -= SPEED
        player.find_animation('rear').active = True
        is_side = False
        player.flip_sprite_x = False
        old_image = image2
        sword.angle = 90
        win.list_objects.remove(sword), win.list_objects.insert(win.list_objects.index(player), sword), check1()

        if sword.pos[0] < 0:
            sword.pos[0] = -sword.pos[0]
    elif input_k(leha.K_s) and not TRADE:
        move_vec[1] += SPEED
        player.find_animation('front').active = True
        is_side = False
        player.flip_sprite_x = False
        old_image = image1
        sword.angle = -90
        win.list_objects.remove(sword), win.list_objects.insert(win.list_objects.index(player) + 1, sword), check2()
        if sword.pos[0] < 0:
            sword.pos[0] = -sword.pos[0]
    if input_k(leha.K_a) and not TRADE:
        move_vec[0] += SPEED
        if is_side:
            player.find_animation('side').active = True
            player.flip_sprite_x = True
            old_image = image3
            sword.angle = 180
            win.list_objects.remove(sword), win.list_objects.insert(win.list_objects.index(player) + 1, sword), check3()
            if sword.pos[0] > 0:
                sword.pos[0] = -sword.pos[0]
    elif input_k(leha.K_d) and not TRADE:
        move_vec[0] -= SPEED
        if is_side:
            player.find_animation('side').active = True
            player.flip_sprite_x = False
            old_image = image3
            sword.angle = 0
            win.list_objects.remove(sword), win.list_objects.insert(win.list_objects.index(player) + 1, sword), check3()
            if sword.pos[0] < 0:
                sword.pos[0] = -sword.pos[0]
    an = sword.find_animation('attack')
    if an:
        if input_k(leha.K_SPACE):
            an.active = True
        elif an.active:
            sword.image = leha.transform.scale(an.frames[0], (sword.size[0], sword.size[1]))
            sword.sprite_copy = sword.image
            an.active = False
    if not input_k(leha.K_a) and not input_k(leha.K_w) and not input_k(leha.K_s) and not input_k(leha.K_d) and old_image:
        player.set_image(old_image)
    camera.move(move_vec, 1)


FPS = 90
old_image = ''
win = Window([1707, 1067], "KYKYMBER", full_sc=True, fps=70)
camera = win.camera
player = win.find_object_of_name('Player')
sword = win.find_object_of_name('sword')
back_trade = win.find_object_of_name('back_panel')

button1 = win.find_object_of_name('button1')
button2 = win.find_object_of_name('button2')
hp_txt_tr = win.find_object_of_name('hp_txt_tr')
hp_txt_tr_1 = win.find_object_of_name('hp_txt_tr_1')
hp_txt_tr_2 = win.find_object_of_name('hp_txt_tr_2')
hp_txt_tr_3 = win.find_object_of_name('hp_txt_tr_3')
hp_img = win.find_object_of_name('hp_img')
damage_img = win.find_object_of_name('damage_img')

text_dialog = win.find_object_of_name('text_dialog')
avatar_trade = win.find_object_of_name('avatar')
sword.set_parent(player)
menu_objects = [win.find_object_of_name('menu_back'),
                win.find_object_of_name('button_menu_play'),
                win.find_object_of_name('button_menu_about'),
                win.find_object_of_name('button_menu_exit')]
image1 = leha.image.load(win.path_delta + "images/Player1_1.png" if win.b else "images/Player1_1.png")
image2 = leha.image.load(win.path_delta + "images/Player2_1.png" if win.b else "images/Player2_1.png")
image3 = leha.image.load(win.path_delta + "images/Player3_1.png" if win.b else "images/Player3_1.png")
skeleton_1 = leha.image.load(win.path_delta + "images/skeleton_1.png" if win.b else "images/skeleton_1.png")
skeleton_2 = leha.image.load(win.path_delta + "images/skeleton_21.png" if win.b else "images/skeleton_21.png")
skeleton_3 = leha.image.load(win.path_delta + "images/skeleton_31.png" if win.b else "images/skeleton_31.png")
image_npc = leha.image.load(win.path_delta + "images/NPC1.png" if win.b else "images/NPC1.png")
image_npc2 = leha.image.load(win.path_delta + "images/NPC2.png" if win.b else "images/NPC2.png")
old_del = sword.pos[1]
DIALOG1 = [['Приветствую тебя, путник!', image_npc], ['Привет, старче.', image1],
               ['У меня как раз есть работа для такого храбреца, как ты.', image_npc], ['Что нужно сделать?', image1],
               ['В наших краях завелось очень много нечисти.', image_npc],
           ['Победи 10 скелетов и я награжу тебя.', image_npc]]
DIALOG2 = [['Возвращайся, когда 10 скелетов будут убиты!', image_npc]]
DIALOG3 = [['Ты справился, я не сомнивался в твоей доблести!', image_npc], ['За проделанную тобой работу возьми эти 100 золотых!', image_npc]]
DIALOG4 = [['У меня для тебя пока нет заданий!', image_npc]]
DIALOG_TRADE = [['Привет, путник.', image_npc2],
                ['Я могу подлечить твои раны, либо улучшить твое оружие.', image_npc2]]
DIALOG = DIALOG1
win.add_object_in_camera(player)
fps_text = win.find_object_of_name('textfps')
hp_text = win.find_object_of_name('texthp_1')
hp_bar = win.find_object_of_name('HPbar1')
score_text = win.find_object_of_name('text_score')
gold_text = win.find_object_of_name('text_gold')
k_w = hp_bar.size[0] / HEALTH
clone_bar = win.find_object_of_name('HPbarSceleton')
vz_ = win.find_object_of_name('vzriv')
cur = 0
while check_run():
    cur = get_current_time()
    fp = win.get_fps()
    SPEED = round(SPEED_CONST * FPS / (fp if fp > 0 else 90))
    SPEED_NPC = round(SPEED_NPC_CONST * FPS / (fp if fp > 0 else 1))
    win.fill_window((78, 156, 22))
    win.update_game_objects()
    fps_text.Text.set_text("Fps:" + str(round(fp))), gold_text.Text.set_text("Gold:" + str(GOLD)), score_text.Text.set_text("Score:" + str(SCORE)), hp_text.Text.set_text(f"X{LIFE}")
    win.update_window()

quit_app()