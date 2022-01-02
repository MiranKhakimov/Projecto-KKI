import time

import pygame, sqlite3, random
from random import randint


if __name__ == '__main__':
    pygame.init()

con = sqlite3.connect("Game_base.db")
cur = con.cursor()


size = 600, 600

bg = pygame.image.load("bg_black.jpg")
card_back = pygame.image.load("card_back.png")
bestiary = pygame.image.load("bestiary.PNG")
menu_plate = pygame.image.load("menu_plate.png")
butt = pygame.image.load("butt_pic.png")
butt_pres = pygame.image.load("butt_clicked.png")
slot_card = pygame.image.load("slot_card.png")
slot_card_proz = pygame.image.load("slot_card_proz.png")
edging = pygame.image.load("edging.png")
ur_at_point = pygame.image.load("health_bar_blue.png")
his_at_point = pygame.image.load("health_bar_red.png")
his_more = pygame.image.load("his_more.png")
ur_more = pygame.image.load("ur_more.png")
equals = pygame.image.load("equals.png")
settings_bg = pygame.image.load("settings_bg.jpg")
tupo_pent = pygame.image.load("pentagramus.png")
attack_sound = pygame.mixer.Sound("attack_sound.mp3")

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.flip()
w, h = pygame.display.get_surface().get_size()

card_show = butt
display_diametr = int((w ** 2 + h ** 2) ** 0.5)
print(display_diametr)
text_size = int(display_diametr * 0.013)
print(text_size)

sword_attack = []
pentagram = []

index = 0
volume_bar = []
volume_index = 5
volume = 1
pymixer = pygame.mixer.music
bg_music = ["Trapper.mp3", "Artileria.mp3", "Burzum-2.mp3",
            "Burzum-3.mp3", "Burzum-4.mp3", "Burzum-5.mp3",
            "STS-1.mp3", "STS-2.mp3", "STS-3.mp3"]

bg_music_index = ['Inscryption - The Trapper', 'AAArtileria', 'Burzum - A Thulean Perspective',
                  'Burzum - The Road To Hell', 'Burzum - The Sacred Well',
                  'Burzum - ForeBears', 'Slay The Spire OST - Exordium',
                  'Slay The Spire OST - Escape Plan', 'Slay The Spire OST - The City']

for i in range(15):
    photo = pygame.image.load("sword_attack_{}.png".format(i + 1))
    photo = pygame.transform.scale(photo, (int(h * 0.296) / 1.5, int(h * 0.296) / 1.5))
    sword_attack.append(photo)

for i in range(22):
    photo = pygame.image.load("pent_{}.png".format(i + 1))
    photo = pygame.transform.scale(photo, (int(w * 0.109), int(w * 0.109)))
    pentagram.append(photo)

for i in range(6):
    photo = pygame.image.load("sound_bar_{}.png".format(i))
    photo = pygame.transform.scale(photo, (int(w * 0.31), int(h * 0.185)))
    volume_bar.append(photo)


print(w, h)
bg = pygame.transform.scale(bg, (w, h))
menu_plate = pygame.transform.scale(menu_plate, (int(w * 0.292), int(h * 0.687)))
settings_bg = pygame.transform.scale(settings_bg, (w, h))
edging = pygame.transform.scale(edging, (int(w * 0.109), int(h * 0.296)))
ur_at_point = pygame.transform.scale(ur_at_point, (int(w * 0.109), int(w * 0.109)))
his_at_point = pygame.transform.scale(his_at_point, (int(w * 0.109), int(w * 0.109)))
his_more = pygame.transform.scale(his_more, (int(w * 0.072), int(w * 0.072)))
ur_more = pygame.transform.scale(ur_more, (int(w * 0.072), int(w * 0.072)))
equals = pygame.transform.scale(equals, (int(w * 0.072), int(w * 0.072)))

slot_card = pygame.transform.scale(slot_card, (int(w * 0.109), int(h * 0.296)))
slot_card_proz = pygame.transform.scale(slot_card_proz, (int(w * 0.136), int(h * 0.37)))
screen.blit(bg, (0, 0))
pygame.display.update()

coord_slots = []
cache_1 = [bg, 0, bg, 0, bg, 0, bg, 0]
cache_2 = [bg, 0, bg, 0, bg, 0, bg, 0]
cache_3 = [bg, 0, bg, 0, bg, 0, bg, 0]
cache_hold = [0, 0, 0, 0]

death_cache_1 = [0, 0, 0, 0]
death_cache_2 = [0, 0, 0, 0]
death_coord_1 = [[], [], [], []]
death_coord_2 = [[], [], [], []]

wrok_cache = [0, 0, 0, 0, 0, 0, 0, 0]

card_places = [1, 1]

func_choice = 0
pos_abil = 0
koeff_ur = 1
koeff_his = 1

pymixer.load("{}".format(bg_music[index]))
pymixer.play(loops=-1)


class Button:
    def __init__(self, width, height, x, y, message, x_m, y_m, font=text_size, font_color=(0, 0, 0)):
        self.font_color = font_color
        self.width = width
        self.height = height
        self.act_cl = butt
        self.inact_cl = butt_pres
        self.message = message
        self.x = x
        self.y = y
        self.x_m = x_m
        self.y_m = y_m
        self.font = font

    def draw_close(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            cache = pygame.transform.scale(butt_pres, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
            if click[0] == 1:
                game = False
                pygame.quit()
                quit()
        else:
            cache = pygame.transform.scale(butt, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
        print_text(self.message, self.x_m, self.y_m, self.font, self.font_color)

    def draw_start(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            cache = pygame.transform.scale(butt_pres, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
            if click[0] == 1:
                table_restart()
                run_game()
                table_create()
        else:
            cache = pygame.transform.scale(butt, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
        print_text(self.message, self.x_m, self.y_m, self.font, self.font_color)

    def draw_back(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            cache = pygame.transform.scale(butt_pres, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
            if click[0] == 1:
                run_menu()
        else:
            cache = pygame.transform.scale(butt, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
        print_text(self.message, self.x_m, self.y_m, self.font, self.font_color)

    def draw_settings(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            cache = pygame.transform.scale(butt_pres, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
            if click[0] == 1:
                run_settings()
        else:
            cache = pygame.transform.scale(butt, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
        print_text(self.message, self.x_m, self.y_m, self.font, self.font_color)

    def draw_turn(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            cache = pygame.transform.scale(butt_pres, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
            if click[0] == 1:
                card_places[0] = 1
                turn()
        else:
            cache = pygame.transform.scale(butt, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
        print_text(self.message, self.x_m, self.y_m, self.font, self.font_color)

    def opening_lootbox(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x <= int(mouse[0]) <= int(self.x + self.width) and self.y < int(mouse[1]) < self.y + self.height:
            cache = pygame.transform.scale(butt_pres, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
            if click[0] == 1:
                lootbox_opens()
        else:
            cache = pygame.transform.scale(butt, (self.width, self.height))
            screen.blit(cache, (self.x, self.y))
        print_text(self.message, self.x_m, self.y_m, self.font, self.font_color)

    def otrisovka(self):
        cache = pygame.transform.scale(butt, (self.width, self.height))
        screen.blit(cache, (self.x, self.y))
        print_text(self.message, self.x_m, self.y_m, self.font, self.font_color)


class SettingsButton:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def music_change(self):
        global index
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x1 <= mouse[0] <= self.x2 and self.y1 < mouse[1] < self.y2:
            if click[0] == 1:
                index += 1
                if index >= len(bg_music_index):
                    index = 0
                pymixer.load("{}".format(bg_music[index]))
                pymixer.play(loops=-1)
            elif click[2] == 1:
                index -= 1
                if index <= 0:
                    index = len(bg_music_index) - 1
                pymixer.load("{}".format(bg_music[index]))
                pymixer.play(loops=-1)

    def volume_change(self):
        global volume_index
        global volume
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x1 <= mouse[0] <= self.x2 and self.y1 < mouse[1] < self.y2:
            if click[0] == 1:
                volume_index += 1
                volume += 0.2
                if volume_index >= len(volume_bar):
                    volume_index = 0
                    volume = 0
            elif click[2] == 1:
                volume_index -= 1
                volume -= 0.2
                if volume_index < 0:
                    volume_index = len(volume_bar) - 1
                    volume = 1
            pymixer.set_volume(volume)

    def open_lootbox(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x1 <= mouse[0] <= self.x2 and self.y1 < mouse[1] < self.y2:
            if click[0] == 1:
                run_lootbox()


def print_text(message, x, y, font_size, font_color=(0, 0, 0), font_type="Palatino Linotype.ttf"):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))

drop = []

def lootbox_opens():
    global drop
    do = """SELECT data FROM inventory WHERE name = 'money'"""
    money = cur.execute(do).fetchall()[0][0]
    if int(money) >= 100:
        do = """UPDATE inventory SET data = {} WHERE name = 'money'""".format(int(money) - 100)
        cur.execute(do)
        drop = []
        for i in range(4):
            card = 0
            x = True
            while x:
                x = False
                card = random.randint(1, 30)
                if card in drop:
                    x = True
                elif card == 26 or card == 27:
                    x = True
                do = """SELECT data FROM inventory WHERE name = {}""".format(card)
                kolvo = cur.execute(do).fetchall()[0][0]
                if kolvo >= 2:
                    x = True
            do = """SELECT name FROM cards WHERE key = {}""".format(card)
            name = cur.execute(do).fetchall()[0][0]
            photo = pygame.image.load("{}_stats.png".format(name))
            photo = pygame.transform.scale(photo, (int(w * 0.109), int(h * 0.296)))
            drop.append(card)
            drop.append(photo)
        for i in range(21):
            screen.blit(bg, (0, 0))
            screen.blit(pygame.transform.scale(tupo_pent, (int(h * 0.7), int(h * 0.7))),
                        (int(w // 2) - int(h * 0.7 * 0.5), int(h // 2) - int(h * 0.7 * 0.5)))
            screen.blit(drop[1], (int(w // 2) - int(w * 0.109 * 0.5) - i * int(w * 0.17 / 21), int(h // 2) - int(h * 0.47) + i * int(h * 0.255 / 21)))
            screen.blit(drop[3], (int(w // 2) - int(w * 0.109 * 0.5) + i * int(w * 0.17 / 21), int(h // 2) - int(h * 0.47) + i * int(h * 0.255 / 21)))
            screen.blit(drop[5], (int(w // 2) - int(w * 0.109 * 0.5) - i * int(w * 0.118 / 21), int(h // 2) - int(h * 0.47) + i * int(h * 0.625 / 21)))
            screen.blit(drop[7], (int(w // 2) - int(w * 0.109 * 0.5) + i * int(w * 0.118 / 21), int(h // 2) - int(h * 0.47) + i * int(h * 0.625 / 21)))
            pygame.draw.rect(screen, "white", (
            int(w // 2) - int(w * 0.109 * 0.5) - 5, int(h // 2) - int(h * 0.47) - 5, int(w * 0.109) + 10,
            int(h * 0.296) + 10))
            print((int(w // 2) - int(w * 0.109 * 0.5) - i * int(w * 0.17 / 20), int(h // 2) - int(h * 0.47) + i * int(h * 0.255 / 20)))
            screen.blit(pygame.transform.scale(bestiary, (int(w * 0.109), int(h * 0.296))),
                        (int(w // 2) - int(w * 0.109 * 0.5), int(h // 2) - int(h * 0.47)))
            pygame.display.update()
        for i in range(4):
            do = """SELECT data FROM inventory WHERE name = {}""".format(drop[i * 2])
            number = cur.execute(do).fetchall()[0][0]
            do = """UPDATE inventory SET data = {} WHERE name = {}""".format(int(number) + 1, drop[i * 2])
            cur.execute(do)
        #con.commit()
        time.sleep(1)

def table_restart():
    global cache_1, cache_2, cache_3, cache_hold, coord_slots_hand, coord_slots, card_places
    coord_slots = []
    cache_1 = [bg, 0, bg, 0, bg, 0, bg, 0]
    cache_2 = [bg, 0, bg, 0, bg, 0, bg, 0]
    cache_3 = [bg, 0, bg, 0, bg, 0, bg, 0]
    cache_hold = [0, 0, 0, 0]
    card_places = [1, 1]
    start = int(w / 2 - int(w * 0.0065) - 2 * int(w * 0.109)), int(h / 2 - 3 - int(h * 0.296))
    for i in range(4):
        coord = start[0] + i * (int(w * 0.109) + int(w * 0.0043)), start[1]
        coord_slots.append(coord)
    for i in range(4):
        coord = start[0] + i * (int(w * 0.109) + int(w * 0.0043)), start[1] + (int(h * 0.296) + int(h * 0.0078))
        coord_slots.append(coord)
    start = int(w / 2 - int(w * 0.0065) - 2 * int(w * 0.136)), int(h / 2 + int(h * 0.37) - int(h * 0.0195))
    for i in range(4):
        coord = start[0] + i * (int(w * 0.136) + int(w * 0.0043)), start[1]
        coord_slots.append(coord)


def table_create():
    global death_coord_1, death_coord_2
    start = int(w / 2 - int(w * 0.0065) - 2 * int(w * 0.109)), \
            int(h / 2 - int(h * 0.0039) - int(h * 0.296))
    screen.blit(bg, (0, 0))
    global coord_slots
    for i in range(4):
        global cache_1
        do = """SELECT data FROM gaming_table WHERE slot = 'his_{}' """.format(i + 1)
        result = cur.execute(do).fetchall()[0][0]
        if result == 0:
            coord = start[0] + i * (int(w * 0.109) + int(w * 0.0043)), start[1]
            if death_cache_1[i] == 1:
                screen.blit(slot_card, (coord))
                coord = death_coord_1[i][0], death_coord_1[i][1]
                screen.blit(cache_1[int(i * 2)], (coord))
            else:
                screen.blit(slot_card, (coord))
        else:
            if int(cache_1[i * 2 + 1]) != result:
                do = """SELECT name FROM cards 
                WHERE key = (SELECT data FROM gaming_table WHERE slot = 'his_{}')""".format(i + 1)
                result_2 = cur.execute(do).fetchall()[0][0]
                card_on_t = pygame.image.load("{}.png".format(result_2))
                card_on_t = pygame.transform.scale(card_on_t, (int(w * 0.109), int(h * 0.296)))
                coord = start[0] + i * (int(w * 0.109) + int(w * 0.0043)), start[1]
                if death_cache_1[i] == 1:
                    coord = death_coord_1[i][0], death_coord_1[i][1]
                screen.blit(card_on_t, (coord))
                cache_1[int(i * 2)] = card_on_t
                cache_1[i * 2 + 1] = result
                do_1 = """SELECT health from gaming_table where slot = 'his_{}'""".format(i + 1)
                result_2 = cur.execute(do_1).fetchall()[0][0]
                if len(str(result_2)) == 1:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i + 1) - int(w * 0.0183),
                               start[1] + int(h * 0.296) - int(h * 0.026), int(text_size * 0.8))
                else:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i + 1) - int(w * 0.0204),
                               start[1] + int(h * 0.296) - int(h * 0.026), int(text_size * 0.8))
                do_2 = """SELECT attack from gaming_table where slot = 'his_{}'""".format(i + 1)
                result_2 = cur.execute(do_2).fetchall()[0][0]
                if len(str(result_2)) == 1:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i) + int(w * 0.008),
                               start[1] + int(h * 0.296) - int(h * 0.026), int(text_size * 0.8))
                else:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i) + int(w * 0.0058),
                               start[1] + int(h * 0.296) - int(h * 0.026), int(text_size * 0.8))
            else:
                coord = start[0] + i * (int(w * 0.109) + int(w * 0.0043)), start[1]
                if death_cache_1[i] == 1:
                    coord = death_coord_1[i][0], death_coord_1[i][1]
                screen.blit(cache_1[int(i * 2)], (coord))
                cache_1[i * 2 + 1] = result
                do_1 = """SELECT health from gaming_table where slot = 'his_{}'""".format(i + 1)
                result_2 = cur.execute(do_1).fetchall()[0][0]
                if len(str(result_2)) == 1:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i + 1) - int(w * 0.0183),
                               start[1] + int(h * 0.296) - int(h * 0.026), int(text_size * 0.8))
                else:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i + 1) - int(w * 0.0204),
                               start[1] + int(h * 0.296) - int(h * 0.026), int(text_size * 0.8))
                do_2 = """SELECT attack from gaming_table where slot = 'his_{}'""".format(i + 1)
                result_2 = cur.execute(do_2).fetchall()[0][0]
                if len(str(result_2)) == 1:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i) + int(w * 0.008),
                               start[1] + int(h * 0.296) - int(h * 0.026), int(text_size * 0.8))
                else:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i) + int(w * 0.0058),
                               start[1] + int(h * 0.296) - int(h * 0.026), int(text_size * 0.8))
    for i in range(4):
        global cache_2
        do = """SELECT data FROM gaming_table WHERE slot = 'ur_{}' """.format(i + 1)
        result = cur.execute(do).fetchall()[0][0]
        if result == 0:
            coord = start[0] + i * (int(w * 0.109) + int(w * 0.0043)), start[1] + (int(h * 0.296) + (int(h * 0.0078)))
            if death_cache_2[i] == 1:
                screen.blit(slot_card, (coord))
                coord = death_coord_2[i][0], death_coord_2[i][1]
                screen.blit(cache_2[int(i * 2)], (coord))
            else:
                screen.blit(slot_card, (coord))
        else:
            if int(cache_2[i * 2 + 1]) != result:
                do = """SELECT name FROM cards 
                WHERE key = (SELECT data FROM gaming_table WHERE slot = 'ur_{}')""".format(i + 1)
                result_2 = cur.execute(do).fetchall()[0][0]
                card_on_t = pygame.image.load("{}.png".format(result_2))
                card_on_t = pygame.transform.scale(card_on_t, (int(w * 0.109), int(h * 0.296)))
                coord = start[0] + i * (int(w * 0.109) + int(w * 0.0043)), start[1] + (int(h * 0.296) + (int(h * 0.0078)))
                if death_cache_2[i] == 1:
                    coord = death_coord_2[i][0], death_coord_2[i][1]
                screen.blit(card_on_t, (coord))
                cache_2[int(i * 2)] = card_on_t
                cache_2[i * 2 + 1] = result
                do_1 = """SELECT health from gaming_table where slot = 'ur_{}'""".format(i + 1)
                result_2 = cur.execute(do_1).fetchall()[0][0]
                if len(str(result_2)) == 1:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i + 1) - int(w * 0.0183),
                               start[1] + int(h * 0.296) * 2 - int(h * 0.0182), int(text_size * 0.8))
                else:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i + 1) - int(w * 0.0204),
                               start[1] + int(h * 0.296) * 2 - int(h * 0.0182), int(text_size * 0.8))
                do_2 = """SELECT attack from gaming_table where slot = 'ur_{}'""".format(i + 1)
                result_2 = cur.execute(do_2).fetchall()[0][0]
                if len(str(result_2)) == 1:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i) + int(w * 0.008),
                               start[1] + int(h * 0.296) * 2 - int(h * 0.0182), int(text_size * 0.8))
                else:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i) + int(w * 0.0058),
                               start[1] + int(h * 0.296) * 2 - int(h * 0.0182), int(text_size * 0.8))
            else:
                coord = start[0] + i * (int(w * 0.109) + int(w * 0.0043)), start[1] + (int(h * 0.296) + int(h * 0.0078))
                if death_cache_2[i] == 1:
                    coord = death_coord_2[i][0], death_coord_2[i][1]
                screen.blit(cache_2[int(i * 2)], (coord))
                cache_2[i * 2 + 1] = result
                do_1 = """SELECT health from gaming_table where slot = 'ur_{}'""".format(i + 1)
                result_2 = cur.execute(do_1).fetchall()[0][0]
                if len(str(result_2)) == 1:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i + 1) - int(w * 0.0183),
                               start[1] + int(h * 0.296) * 2 - int(h * 0.0182), int(text_size * 0.8))
                else:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i + 1) - int(w * 0.0204),
                               start[1] + int(h * 0.296) * 2 - int(h * 0.0182), int(text_size * 0.8))
                do_2 = """SELECT attack from gaming_table where slot = 'ur_{}'""".format(i + 1)
                result_2 = cur.execute(do_2).fetchall()[0][0]
                if len(str(result_2)) == 1:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i) + int(w * 0.008),
                               start[1] + int(h * 0.296) * 2 - int(h * 0.0182), int(text_size * 0.8))
                else:
                    print_text(str(result_2), start[0] + (int(w * 0.109) + int(w * 0.0043)) * (i) + int(w * 0.0058),
                               start[1] + int(h * 0.296) * 2 - int(h * 0.0182), int(text_size * 0.8))
    start = int(w / 2 - int(w * 0.0065) - 2 * int(w * 0.136)), int(h / 2 + int(h * 0.37) - int(h * 0.0195))
    for i in range(4):
        global cache_3, cache_hold
        if cache_hold[i] == 0:
            do = """SELECT data FROM gaming_table WHERE slot = 'ur_hand_{}' """.format(i + 1)
            result = cur.execute(do).fetchall()[0][0]
            if result == 0:
                coord = start[0] + i * (int(w * 0.136) + int(w * 0.0043)), start[1]
                screen.blit(slot_card_proz, (coord))
            else:
                if int(cache_3[i * 2 + 1]) != result:
                    do = """SELECT name FROM cards 
                            WHERE key = (SELECT data FROM gaming_table WHERE slot = 'ur_hand_{}')""".format(i + 1)
                    result_2 = cur.execute(do).fetchall()[0][0]
                    card_on_t = pygame.image.load("{}.png".format(result_2))
                    card_on_t = pygame.transform.scale(card_on_t, (int(w * 0.136), int(h * 0.37)))
                    coord = start[0] + i * (int(w * 0.136) + int(w * 0.0043)), start[1]
                    screen.blit(card_on_t, (coord))
                    cache_3[int(i * 2)] = card_on_t
                    cache_3[i * 2 + 1] = result
                else:
                    coord = start[0] + i * (int(w * 0.136) + int(w * 0.0043)), start[1]
                    screen.blit(cache_3[int(i * 2)], (coord))
                    cache_3[i * 2 + 1] = result
        else:
            coord = start[0] + i * (int(w * 0.136) + int(w * 0.0043)), start[1]
            screen.blit(slot_card_proz, (coord))
    screen.blit(his_at_point, (int(w / 2) + int(w * 0.109) * 2, int(h / 2) - int(h * 0.296 / 2) - int(w * 0.109 / 2)))
    screen.blit(ur_at_point, (int(w / 2) + int(w * 0.109) * 2, int(h / 2) + int(h * 0.296 / 2) - int(w * 0.109 / 2)))
    p_at1 = """SELECT data FROM gaming_table WHERE slot = 'his_at'"""
    p_at2 = """SELECT data FROM gaming_table WHERE slot = 'ur_at'"""
    pers_at1 = cur.execute(p_at1).fetchall()[0][0]
    pers_at2 = cur.execute(p_at2).fetchall()[0][0]
    if len(str(pers_at1)) == 1:
        print_text(str(pers_at1), int(w / 2) + int(w * 0.131) * 2, int(h / 2) - int(h * 0.296 / 2) - int(w * 0.105 / 4), int(text_size * 3))
    elif len(str(pers_at1)) == 2:
        print_text(str(pers_at1), int(w / 2) + int(w * 0.125) * 2, int(h / 2) - int(h * 0.296 / 2) - int(w * 0.105 / 4), int(text_size * 3))
    else:
        print_text(str(pers_at1), int(w / 2) + int(w * 0.120) * 2, int(h / 2) - int(h * 0.296 / 2) - int(w * 0.105 / 4),
                   int(text_size * 3))
    if len(str(pers_at2)) == 1:
        print_text(str(pers_at2), int(w / 2) + int(w * 0.131) * 2, int(h / 2) + int(h * 0.296 / 2) - int(w * 0.105 / 4), int(text_size * 3))
    elif len(str(pers_at2)) == 2:
        print_text(str(pers_at2), int(w / 2) + int(w * 0.125) * 2, int(h / 2) + int(h * 0.296 / 2) - int(w * 0.105 / 4), int(text_size * 3))
    else:
        print_text(str(pers_at2), int(w / 2) + int(w * 0.120) * 2, int(h / 2) + int(h * 0.296 / 2) - int(w * 0.105 / 4),
                   int(text_size * 3))
    if pers_at1 == pers_at2:
        screen.blit(equals, (int(w / 2) + int(w * 0.109) * 2 + int(w * 0.032),
                             int(h / 2) - int(w * 0.072 / 2)))
    if pers_at1 > pers_at2:
        screen.blit(his_more, (int(w / 2) + int(w * 0.109) * 2 + int(w * 0.032),
                             int(h / 2) - int(w * 0.072 / 2)))
        print_text("{}".format(pers_at1 - pers_at2), int(w / 2) + int(w * 0.109) * 2 + int(w * 0.075),
                                                      int(h / 2) - int(w * 0.015), int(text_size * 2.5), (255, 255, 255))
    if pers_at1 < pers_at2:
        screen.blit(ur_more, (int(w / 2) + int(w * 0.109) * 2 + int(w * 0.032),
                             int(h / 2) - int(w * 0.072 / 2)))
        print_text("{}".format(pers_at2 - pers_at1), int(w / 2) + int(w * 0.109) * 2 + int(w * 0.075),
                   int(h / 2) - int(w * 0.015), int(text_size * 2.5), (255, 255, 255))


def table_active():
    global coord_slots, cache_hold, card_show
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0] == 0:
        if 1 in cache_hold:
            for i in range(4):
                c_s = coord_slots[i + 4]
                if int(c_s[0]) <= int(mouse[0]) <= int(w * 0.109) + int(c_s[0]) and \
                        int(c_s[1]) <= int(mouse[1]) <= int(h * 0.296) + int(c_s[1]):
                    if cache_2[i * 2 + 1] == 0:
                        do = """SELECT data FROM gaming_table 
                        WHERE slot = 'ur_hand_{}' """.format(cache_hold.index(1) + 1)
                        result = cur.execute(do).fetchall()[0][0]
                        if result == 8 or result == 21 or result == 22 or result == 23 or result == 24 or result == 25:
                            gold_dragon()
                        if result == 16:
                            do = """UPDATE gaming_table SET ability = 1 WHERE slot = 'ur_{}'""".format(i + 1)
                            cur.execute(do)
                        do_hp = """SELECT health from cards where key = {}""".format(result)
                        hp = cur.execute(do_hp).fetchall()[0][0]
                        do_at = """SELECT attack from cards where key = {}""".format(result)
                        at = cur.execute(do_at).fetchall()[0][0]
                        do_2 = """UPDATE gaming_table SET data = {} WHERE slot = 'ur_{}' """.format(result, i + 1)
                        cur.execute(do_2)
                        do_2_hp = """UPDATE gaming_table SET health = {} WHERE slot = 'ur_{}' """.format(hp, i + 1)
                        cur.execute(do_2_hp)
                        do_2_at = """UPDATE gaming_table SET attack = {} WHERE slot = 'ur_{}' """.format(at, i + 1)
                        cur.execute(do_2_at)
                        do_3 = """UPDATE gaming_table SET data = 0 
                        WHERE slot = 'ur_hand_{}' """.format(cache_hold.index(1) + 1)
                        cur.execute(do_3)
                        card_ability(result, i + 1)
                    cache_hold = [0, 0, 0, 0]
            cache_hold = [0, 0, 0, 0]
        else:
            for i in range(12):
                c_s = coord_slots[i]
                if i < 8:
                    if int(c_s[0]) <= int(mouse[0]) <= int(w * 0.109) + int(c_s[0]) and \
                            int(c_s[1]) <= int(mouse[1]) <= int(h * 0.296) + int(c_s[1]):
                        if 7 >= i >= 4:
                            do = """SELECT data FROM gaming_table WHERE slot = 'ur_{}' """.format(i - 4 + 1)
                        else:
                            do = """SELECT data FROM gaming_table WHERE slot = 'his_{}' """.format(i + 1)
                        result = cur.execute(do).fetchall()[0][0]
                        if result != "0":
                            if 7 >= i >= 4:
                                do = """SELECT name FROM cards 
                                WHERE key = (SELECT data FROM gaming_table WHERE slot = 'ur_{}')""".format(i - 4 + 1)
                            else:
                                do = """SELECT name FROM cards 
                                WHERE key = (SELECT data FROM gaming_table WHERE slot = 'his_{}')""".format(i + 1)
                            if cur.execute(do).fetchall() != []:
                                result_2 = cur.execute(do).fetchall()[0][0]
                                card_show = pygame.image.load("{}_stats.png".format(result_2))
                                card_show = pygame.transform.scale(card_show, (int(w * 0.101) * 2.5, int(h * 0.278) * 2.5))
                                screen.blit(card_show, (0, h/2 - int(h * 0.278) * 1.25))
                                break
                else:
                    if int(c_s[0]) <= int(mouse[0]) <= int(w * 0.136) + int(c_s[0]) and \
                            int(c_s[1]) <= int(mouse[1]) <= int(h * 0.37) + int(c_s[1]):
                        do = """SELECT data FROM gaming_table WHERE slot = 'ur_hand_{}' """.format(i - 8 + 1)
                        result = cur.execute(do).fetchall()[0][0]
                        if result != "0":
                            do = """SELECT name FROM cards 
                            WHERE key = (SELECT data FROM gaming_table WHERE slot = 'ur_hand_{}')""".format(i - 8 + 1)
                            if cur.execute(do).fetchall() != []:
                                result_2 = cur.execute(do).fetchall()[0][0]
                                card_show = pygame.image.load("{}_stats.png".format(result_2))
                                card_show = pygame.transform.scale(card_show, (int(w * 0.101) * 2.5, int(h * 0.278) * 2.5))
                                screen.blit(card_show, (0, h/2 - int(h * 0.278) * 1.25))
                                break
    else:
        for i in range(4):
            c_s = coord_slots[i + 8]
            if cache_hold[i] == 1:
                screen.blit(card_show, (mouse[0] - int(w * 0.109 * 0.5), mouse[1] - int(h * 0.296 * 0.5)))
            elif int(c_s[0]) <= int(mouse[0]) <= int(w * 0.136) + int(c_s[0]) and \
                    int(c_s[1]) <= int(mouse[1]) <= int(h * 0.37) + int(c_s[1]):
                do = """SELECT data FROM gaming_table WHERE slot = 'ur_hand_{}' """.format(i + 1)
                result = cur.execute(do).fetchall()[0][0]
                if result != "0":
                    do = """SELECT name FROM cards 
                    WHERE key = (SELECT data FROM gaming_table WHERE slot = 'ur_hand_{}')""".format(i + 1)
                    if cur.execute(do).fetchall() != []:
                        if 1 not in cache_hold:
                            result_2 = cur.execute(do).fetchall()[0][0]
                            card_show = pygame.image.load("{}_stats.png".format(result_2))
                            card_show = pygame.transform.scale(card_show, (int(w * 0.109), int(h * 0.296)))
                            cache_hold[i] = 1
                        card_show = pygame.transform.scale(card_show, (int(w * 0.109), int(h * 0.296)))
                        screen.blit(card_show, (mouse[0] - int(w * 0.109 * 0.5), mouse[1] - int(h * 0.296 * 0.5)))
                        break


def turn():
    global card_places
    for i in range(4):
        do = """SELECT data FROM gaming_table WHERE slot = 'ur_hand_{}' """.format(i + 1)
        result = cur.execute(do).fetchall()[0][0]
        if result == 23:
            dragons = 0
            free_slot = []
            for z in range(4):
                do = """SELECT data FROM gaming_table WHERE slot = 'ur_{}' """.format(z + 1)
                res = cur.execute(do).fetchall()[0][0]
                if res == 0:
                    free_slot.append(z + 1)
                elif res == 8 or res == 21 or res == 22 or res == 23 or res ==  24 or res == 25:
                    dragons += 1
            if dragons >= 2:
                if free_slot != []:
                    do = """UPDATE gaming_table SET data = 0 WHERE slot = 'ur_hand_{}'""".format(i+1)
                    cur.execute(do)
                    target = random.choice(free_slot)
                    do = """UPDATE gaming_table SET data = 23 WHERE slot = 'ur_{}'""".format(target)
                    cur.execute(do)
                    att = """UPDATE gaming_table SET attack = 5 WHERE slot = 'ur_{}'""".format(target)
                    hp = """UPDATE gaming_table SET health = 4 WHERE slot = 'ur_{}'""".format(target)
                    cur.execute(att)
                    cur.execute(hp)
                    gold_dragon()
    card_places[0] = int(card_places[0]) - 1
    if card_places[0] == 0:
        for i in range(4):
            do = """SELECT data FROM gaming_table WHERE slot = 'his_{}' """.format(i + 1)
            result = cur.execute(do).fetchall()[0][0]
            if result == 0:
                while card_places[1] != 0:
                    enemy_card = randint(0, 3)
                    do = """SELECT data FROM gaming_table WHERE slot = 'his_hand_{}' """.format(enemy_card + 1)
                    result = cur.execute(do).fetchall()[0][0]
                    if result != 0:
                        do = """UPDATE gaming_table SET data = 0 WHERE slot = 'his_hand_{}' """.format(enemy_card + 1)
                        cur.execute(do)
                        for i in range(4):
                            do = """SELECT data FROM gaming_table WHERE slot = 'his_{}' """.format(i + 1)
                            result_2 = cur.execute(do).fetchall()[0][0]
                            if result_2 == 0:
                                do_2 = """UPDATE gaming_table SET data = {} WHERE slot = 'his_{}' """.format(result, i + 1)
                                cur.execute(do_2)
                                do_hp = """SELECT health from cards where key = {}""".format(result)
                                hp = cur.execute(do_hp).fetchall()[0][0]
                                do_at = """SELECT attack from cards where key = {}""".format(result)
                                at = cur.execute(do_at).fetchall()[0][0]
                                do_2_hp = """UPDATE gaming_table SET health = {} WHERE slot = 'his_{}' """.format(hp,
                                                                                                                 i + 1)
                                cur.execute(do_2_hp)
                                do_2_at = """UPDATE gaming_table SET attack = {} WHERE slot = 'his_{}' """.format(at,
                                                                                                                 i + 1)
                                cur.execute(do_2_at)
                                card_places[1] = int(card_places[1]) - 1
                                break
        card_places[0] = int(card_places[0]) + 1
        card_places[1] = int(card_places[1]) + 1
        for i in range(4):
            fight(i+1, i+1)
        for i in range(4):
            do = """SELECT data FROM gaming_table WHERE slot = 'his_hand_{}' """.format(i + 1)
            result = cur.execute(do).fetchall()[0][0]
            if result == 0:
                index = randint(1, 30)
                do = """UPDATE gaming_table SET data = {} WHERE slot = 'his_hand_{}' """.format(index, i + 1)
                cur.execute(do)
        for i in range(4):
            do = """SELECT data FROM gaming_table WHERE slot = 'ur_hand_{}' """.format(i + 1)
            result = cur.execute(do).fetchall()[0][0]
            if result == 0:
                index = randint(1, 30)
                do = """UPDATE gaming_table SET data = {} WHERE slot = 'ur_hand_{}' """.format(index, i + 1)
                cur.execute(do)
        for i in range(4):
            do = """SELECT data FROM gaming_table WHERE slot = 'ur_{}' """.format(i + 1)
            result = cur.execute(do).fetchall()[0][0]
            if result == 20:
                do = """SELECT ability FROM gaming_table WHERE slot = 'ur_{}' """.format(i + 1)
                abil = cur.execute(do).fetchall()[0][0]
                abil += 1
                do = """UPDATE gaming_table SET ability = {} WHERE slot = 'ur_{}'""".format(abil, i + 1)
                cur.execute(do)
                if abil == 2:
                    do = """SELECT attack FROM gaming_table WHERE slot = 'ur_{}' """.format(i + 1)
                    att = cur.execute(do).fetchall()[0][0]
                    do = """UPDATE gaming_table SET attack = {} + 8 * {} WHERE slot = 'ur_{}'""".format(att, koeff_ur,
                                                                                                        i + 1)
                    cur.execute(do)
    else:
        card_places[0] -= 1
    drackonchik_func()
    death()


def card_ability(index, position):
    global func_choice, pos_abil, koeff_ur, koeff_his, wrok_cache
    pos_abil = position
    if index == 1:
        sel_h = """SELECT health FROM gaming_table WHERE slot = 'ur_{}'""".format(position + 1)
        if position <= 3:
            heal = cur.execute(sel_h).fetchall()[0][0]
            do = """UPDATE gaming_table SET health = {} + 2 * {} 
            WHERE slot = 'ur_{}' """.format(heal, koeff_ur, position + 1)
            cur.execute(do)
        sel_h = """SELECT health FROM gaming_table WHERE slot = 'ur_{}'""".format(position - 1)
        if position >= 2:
            heal = cur.execute(sel_h).fetchall()[0][0]
            do = """UPDATE gaming_table SET health = {} + 2 * {}
            WHERE slot = 'ur_{}' """.format(heal, koeff_ur, position - 1)
            cur.execute(do)
        turn()
    elif index == 2:
        func_choice = 2
    elif index == 3:
        func_choice = 3
    elif index == 4:
        koff = 0
        for i in range(4):
            do = """SELECT data FROM gaming_table WHERE slot = 'ur_{}'""".format(i+1)
            result = cur.execute(do).fetchall()[0][0]
            if result != 0:
                koff += 1
        koff -= 1
        table_create()
        do = """UPDATE gaming_table SET health = 1 + {} * {} WHERE slot = 'ur_{}'""".format(koff, koeff_ur, position)
        cur.execute(do)
        do = """UPDATE gaming_table SET attack = 1 + 2 * {} * {} WHERE slot = 'ur_{}'""".format(koff, koeff_ur, position)
        cur.execute(do)
        turn()
    elif index == 6:
        do = """SELECT data FROM gaming_table WHERE slot = 'his_{}' """.format(position)
        result = cur.execute(do).fetchall()[0][0]
        if result != 0:
            do = """SELECT attack FROM gaming_table WHERE slot = 'his_{}' """.format(position)
            at_his = cur.execute(do).fetchall()[0][0]
            do = """SELECT attack FROM gaming_table WHERE slot = 'ur_{}' """.format(position)
            at_ur = cur.execute(do).fetchall()[0][0]
            if at_his == 0 or at_his == 1:
                at_ur = at_ur + at_his * koeff_ur
                at_his = 0
            elif at_his >= 2:
                at_his -= 2
                at_ur = at_ur + 2 * koeff_ur
            do = """UPDATE gaming_table SET attack = {} WHERE slot = 'his_{}' """.format(at_his, position)
            cur.execute(do)
            do = """UPDATE gaming_table SET attack = {} WHERE slot = 'ur_{}' """.format(at_ur, position)
            cur.execute(do)
        turn()
    elif index == 7:
        do = """SELECT data FROM gaming_table WHERE slot = 'his_{}' """.format(position)
        result = cur.execute(do).fetchall()[0][0]
        if result != 0:
            do = """SELECT health FROM gaming_table WHERE slot = 'his_{}' """.format(position)
            hp_his = cur.execute(do).fetchall()[0][0]
            hp_his -= 3
            do = """UPDATE gaming_table SET health = {} WHERE slot = 'his_{}'""".format(hp_his, position)
            cur.execute(do)
        death()
        turn()
    elif index == 8:
        drackonchik_func()
        turn()
    elif index == 11:
        if position <= 3:
            sel_h = """SELECT health FROM gaming_table WHERE slot = 'ur_{}'""".format(position + 1)
            heal = cur.execute(sel_h).fetchall()[0][0]
            sel_a = """SELECT attack FROM gaming_table WHERE slot = 'ur_{}'""".format(position + 1)
            att = cur.execute(sel_a).fetchall()[0][0]
            do = """UPDATE gaming_table SET health = {} + 1 * {} WHERE slot = 'ur_{}'""".format(heal, koeff_ur, position + 1)
            cur.execute(do)
            do = """UPDATE gaming_table SET attack = {} + 1  * {} WHERE slot = 'ur_{}'""".format(att, koeff_ur, position + 1)
            cur.execute(do)
        if position >= 2:
            sel_h = """SELECT health FROM gaming_table WHERE slot = 'ur_{}'""".format(position - 1)
            heal = cur.execute(sel_h).fetchall()[0][0]
            sel_a = """SELECT attack FROM gaming_table WHERE slot = 'ur_{}'""".format(position - 1)
            att = cur.execute(sel_a).fetchall()[0][0]
            do = """UPDATE gaming_table SET health = {} + 1 * {} WHERE slot = 'ur_{}'""".format(heal, koeff_ur,
                                                                                                position - 1)
            cur.execute(do)
            do = """UPDATE gaming_table SET attack = {} + 1  * {} WHERE slot = 'ur_{}'""".format(att, koeff_ur,
                                                                                                 position - 1)
            cur.execute(do)
        turn()
    elif index == 12:
        do = """SELECT data FROM gaming_table WHERE slot = 'his_{}' """.format(position)
        result = cur.execute(do).fetchall()[0][0]
        if result != 0:
            do = """SELECT attack FROM gaming_table WHERE slot = 'his_{}' """.format(position)
            at_his = cur.execute(do).fetchall()[0][0]
            if at_his == 0 or at_his == 1 or at_his == 2:
                at_his = 0
            elif at_his >= 3:
                at_his -= 3
            do = """UPDATE gaming_table SET attack = {} WHERE slot = 'his_{}' """.format(at_his, position)
            cur.execute(do)
        turn()
    elif index == 13:
        func_choice = 13
    elif index == 14:
        for i in range(4):
            do = """SELECT health FROM gaming_table WHERE slot = 'his_{}' """.format(i+1)
            result = cur.execute(do).fetchall()[0][0]
            do = """UPDATE gaming_table SET health = {} - 2 WHERE slot = 'his_{}'""".format(result, i+1)
            cur.execute(do)
        for i in range(4):
            if i + 1 != position:
                do = """SELECT health FROM gaming_table WHERE slot = 'ur_{}' """.format(i + 1)
                result = cur.execute(do).fetchall()[0][0]
                do = """UPDATE gaming_table SET health = {} - 2 WHERE slot = 'ur_{}'""".format(result, i + 1)
                cur.execute(do)
        death()
        turn()
    elif index == 16:
        do = """SELECT health FROM cards WHERE key = 16"""
        result = cur.execute(do).fetchall()[0][0]
        wrok_cache[position + 3] = result
        func_choice = 16
    elif index == 18:
        enemy = []
        target = 0
        for i in range(4):
            do = """SELECT data FROM gaming_table WHERE slot = 'his_{}'""".format(i + 1)
            result = cur.execute(do).fetchall()[0][0]
            if result != 0:
                enemy.append(i + 1)
            if enemy != []:
                target = random.choice(enemy)
        if target != 0:
            fight(target, position)
        death()
    elif index == 19:
        func_choice = 19
    elif index == 21:
        for i in range(4):
            do = """SELECT data FROM gaming_table WHERE slot = 'his_{}'""".format(i + 1)
            result = cur.execute(do).fetchall()[0][0]
            if result != 0:
                do = """SELECT health FROM gaming_table WHERE slot = 'his_{}'""".format(i + 1)
                health = cur.execute(do).fetchall()[0][0]
                do = """UPDATE gaming_table SET health = {} - 2 WHERE slot = 'his_{}'""".format(health, i + 1)
                cur.execute(do)
        death()
        turn()
    elif index == 22:
        for i in range(4):
            if i + 1 != position:
                do = """SELECT data FROM gaming_table WHERE slot = 'ur_{}'""".format(i + 1)
                result = cur.execute(do).fetchall()[0][0]
                if result != 0:
                    do = """SELECT health FROM gaming_table WHERE slot = 'ur_{}'""".format(i + 1)
                    health = cur.execute(do).fetchall()[0][0]
                    do = """UPDATE gaming_table SET health = {} + 3 WHERE slot = 'ur_{}'""".format(health, i + 1)
                    cur.execute(do)
        turn()
    elif index == 28:
        func_choice = 28
    elif index == 29:
        card_places[0] = card_places[0] + 2
        do = """UPDATE gaming_table SET health = 0 WHERE slot = 'ur_{}'""".format(position)
        cur.execute(do)
        pent(position, 1)
        death()
    elif index == 30:
        buff = 0
        for i in range(4):
            if i + 1 != position:
                do = """SELECT data FROM gaming_table WHERE slot = 'ur_{}'""".format(i + 1)
                result = cur.execute(do).fetchall()[0][0]
                if result == 10 or result == 14 or result == 15 or result == 16 or result == 17 or result == 18 or result == 19:
                    do = """UPDATE gaming_table SET data = 0 WHERE slot = 'ur_{}'""".format(i + 1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET ability = 0 WHERE slot = 'ur_{}'""".format(i + 1)
                    cur.execute(do)
                    buff += 1
        do = """UPDATE gaming_table SET health = 1 + 3 * {} * {} WHERE slot = 'ur_{}'""".format(buff, koeff_ur, position)
        cur.execute(do)
        do = """UPDATE gaming_table SET attack = 2 + 3 * {} * {} WHERE slot = 'ur_{}'""".format(buff, koeff_ur,
                                                                                                position)
        cur.execute(do)
        death()
        turn()
    elif index == 24:
        func_choice = 24
    else:
        turn()


def daw_func():
    global func_choice, pos_abil, koeff_ur, koeff_his
    cch = cache_1[1::2] + cache_2[1::2]
    if cch[0] == 0 and cch[1] == 0 and cch[2] == 0 and cch[3] == 0 and cch[4] == 0 and cch[5] == 0 and cch[6] == 0 \
            and cch[7] == 0:
        func_choice = 0
        turn()
    else:
        table_create()
        if choice(0) == 1:
            slot = choice(1)
            if slot != 'ur_{}'.format(pos_abil):
                do = """SELECT data FROM gaming_table WHERE slot = '{}'""".format(slot)
                res = cur.execute(do).fetchall()[0][0]
                if res != 0:
                    sel_h = """SELECT health FROM gaming_table WHERE slot = '{}'""".format(slot)
                    heal = cur.execute(sel_h).fetchall()[0][0]
                    sel_a = """SELECT attack FROM gaming_table WHERE slot = '{}'""".format(slot)
                    att = cur.execute(sel_a).fetchall()[0][0]
                    if "ur" in slot:
                        do = """UPDATE gaming_table SET health = {} + 2 * {} WHERE slot = '{}'""".format(heal, koeff_ur, slot)
                        cur.execute(do)
                        do = """UPDATE gaming_table SET attack = {} + 1  * {} WHERE slot = '{}'""".format(att, koeff_ur, slot)
                        cur.execute(do)
                    elif "his" in slot:
                        do = """UPDATE gaming_table SET health = {} + 2 * {} WHERE slot = '{}'""".format(heal, koeff_his,
                                                                                                         slot)
                        cur.execute(do)
                        do = """UPDATE gaming_table SET attack = {} + 1  * {} WHERE slot = '{}'""".format(att, koeff_his,
                                                                                                          slot)
                        cur.execute(do)
                    func_choice = 0
                    turn()


def solar_func(pos):
    global func_choice
    cch = cache_1[1::2] + cache_2[1::2]
    if cch[0] == 0 and cch[1] == 0 and cch[2] == 0 and cch[3] == 0 and cch[4] == 0 and cch[5] == 0 and cch[6] == 0 \
            and cch[7] == 0:
        func_choice = 0
        turn()
    else:
        table_create()
        if choice(0) == 1:
            slot = choice(1)
            do = """SELECT data FROM gaming_table WHERE slot = '{}'""".format(slot)
            res = cur.execute(do).fetchall()[0][0]
            if res != 0:
                do = """SELECT data FROM gaming_table WHERE slot = 'ur_{}'""".format(pos)
                data_1 = cur.execute(do).fetchall()[0][0]
                do = """SELECT data FROM gaming_table WHERE slot = '{}'""".format(slot)
                data_2 = cur.execute(do).fetchall()[0][0]
                if data_2 == 16:
                    if "ur" in slot:
                        wrok_cache[int(slot[-1]) + 3], wrok_cache[pos + 3] = wrok_cache[pos + 3], \
                                                                             wrok_cache[int(slot[-1]) + 3]
                    elif "his" in slot:
                        wrok_cache[int(slot[-1]) - 1], wrok_cache[pos + 3] = wrok_cache[pos + 3], \
                                                                             wrok_cache[int(slot[-1]) - 1]
                    do = """SELECT ability FROM gaming_table WHERE slot = '{}'""".format(slot)
                    abil = cur.execute(do).fetchall()[0][0]
                    if abil == 1:
                        do = """UPDATE gaming_table SET ability = 1 WHERE slot = 'ur_{}'""".format(pos)
                        cur.execute(do)
                        do = """UPDATE gaming_table SET ability = 0 WHERE slot = '{}'""".format(slot)
                        cur.execute(do)
                do = """SELECT health FROM gaming_table WHERE slot = 'ur_{}'""".format(pos)
                hp_1 = cur.execute(do).fetchall()[0][0]
                do = """SELECT attack FROM gaming_table WHERE slot = 'ur_{}'""".format(pos)
                att_1 = cur.execute(do).fetchall()[0][0]
                do = """SELECT health FROM gaming_table WHERE slot = '{}'""".format(slot)
                hp_2 = cur.execute(do).fetchall()[0][0]
                do = """SELECT attack FROM gaming_table WHERE slot = '{}'""".format(slot)
                att_2 = cur.execute(do).fetchall()[0][0]
                update = """UPDATE gaming_table SET data = {} WHERE slot = 'ur_{}' """.format(data_2, pos)
                cur.execute(update)
                update = """UPDATE gaming_table SET data = {} WHERE slot = '{}' """.format(data_1, slot)
                cur.execute(update)
                table_create()
                update = """UPDATE gaming_table SET health = {} WHERE slot = 'ur_{}' """.format(hp_2, pos)
                cur.execute(update)
                update = """UPDATE gaming_table SET health = {} WHERE slot = '{}' """.format(hp_1, slot)
                cur.execute(update)
                update = """UPDATE gaming_table SET attack = {} WHERE slot = 'ur_{}' """.format(att_2, pos)
                cur.execute(update)
                update = """UPDATE gaming_table SET attack = {} WHERE slot = '{}' """.format(att_1, slot)
                cur.execute(update)
                func_choice = 0
                wrok_func()
                turn()


def drackonchik_func():
    global koeff_ur
    koeff_ur = 1
    for i in range(4):
        do = """SELECT data FROM gaming_table WHERE slot = 'ur_{}'""".format(i+1)
        result = cur.execute(do).fetchall()[0][0]
        if result == 8:
            koeff_ur *= 2


def demilich_func():
    global func_choice
    cch = cache_1[1::2] + cache_2[1::2]
    if cch[0] == 0 and cch[1] == 0 and cch[2] == 0 and cch[3] == 0 and cch[4] == 0 and cch[5] == 0 and cch[6] == 0 \
            and cch[7] == 0:
        func_choice = 0
        turn()
    else:
        table_create()
        if choice(0) == 1:
            slot = choice(1)
            do = """SELECT data FROM gaming_table WHERE slot = '{}'""".format(slot)
            res = cur.execute(do).fetchall()[0][0]
            if res != 0:
                do = """UPDATE gaming_table SET health = 0 WHERE slot = '{}'""".format(slot)
                cur.execute(do)
                do = """UPDATE gaming_table SET data = 0 WHERE slot = '{}'""".format(slot)
                cur.execute(do)
                do = """UPDATE gaming_table SET attack = 0 WHERE slot = '{}'""".format(slot)
                cur.execute(do)
                do = """UPDATE gaming_table SET ability = 0 WHERE slot = '{}'""".format(slot)
                cur.execute(do)
                death()
                func_choice = 0
                turn()


def wrok_func():
    global wrok_cache, func_choice
    for i in range(4):
        do = """SELECT data FROM gaming_table WHERE slot = 'ur_{}'""".format(i + 1)
        result = cur.execute(do).fetchall()[0][0]
        if result == 16:
            do = """SELECT health FROM gaming_table WHERE slot = 'ur_{}'""".format(i + 1)
            health = cur.execute(do).fetchall()[0][0]
            if wrok_cache[i + 4] > health:
                do = """SELECT ability FROM gaming_table WHERE slot = 'ur_{}'""".format(i + 1)
                abil = cur.execute(do).fetchall()[0][0]
                if abil == 1:
                    do = """UPDATE gaming_table SET ability = 0 WHERE slot = 'ur_{}'""".format(i + 1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET health = {} WHERE slot = 'ur_{}'""".format(wrok_cache[i + 4], i + 1)
                    cur.execute(do)
        else:
            wrok_cache[i + 4] = 0
    func_choice = 0


def shadow_demon(pos):
    global func_choice, wrok_cache
    cch = cache_1[1::2] + cache_2[1::2]
    if cch[0] == 0 and cch[1] == 0 and cch[2] == 0 and cch[3] == 0 and cch[4] == 0 and cch[5] == 0 and cch[6] == 0 \
            and cch[7] == 0:
        func_choice = 0
        turn()
    else:
        table_create()
        if choice(0) == 1:
            slot = choice(1)
            do = """SELECT data FROM gaming_table WHERE slot = '{}'""".format(slot)
            res = cur.execute(do).fetchall()[0][0]
            if res != 0:
                do = """UPDATE gaming_table SET data = {} WHERE slot = 'ur_{}'""".format(res, pos)
                cur.execute(do)
                if res == 16:
                    wrok_cache[pos + 3] = 2
                    do = """UPDATE gaming_table SET ability = 1 WHERE slot = 'ur_{}'""".format(pos)
                    cur.execute(do)
                func_choice = 0
                turn()


def gold_dragon():
    for z in range(4):
        do = """SELECT data FROM gaming_table WHERE slot = 'ur_{}' """.format(z + 1)
        res = cur.execute(do).fetchall()[0][0]
        if res == 25:
            do = """SELECT health FROM gaming_table WHERE slot = 'ur_{}' """.format(z + 1)
            health = cur.execute(do).fetchall()[0][0]
            do = """SELECT attack FROM gaming_table WHERE slot = 'ur_{}' """.format(z + 1)
            attack = cur.execute(do).fetchall()[0][0]
            att = """UPDATE gaming_table SET attack = {} + 2 * {} 
            WHERE slot = 'ur_{}'""".format(attack, koeff_ur, z + 1)
            hp = """UPDATE gaming_table SET health = {} + 2 * {} 
            WHERE slot = 'ur_{}'""".format(health, koeff_ur, z + 1)
            cur.execute(att)
            cur.execute(hp)


bronz_target_1 = ""
bronz_target_2 = ""


def bronz_dragon():
    global func_choice, bronz_target_1, bronz_target_2
    cch = cache_1[1::2]
    kolvo_card = 0
    for i in range(len(cch)):
        if cch[i] != 0:
            kolvo_card += 1
    if kolvo_card >= 2:
        if bronz_target_1 == "":
            table_create()
            if choice(0) == 1:
                slot = choice(1)
                if "his" in slot:
                    do = """SELECT data FROM gaming_table WHERE slot = '{}'""".format(slot)
                    res = cur.execute(do).fetchall()[0][0]
                    if res != 0:
                        bronz_target_1 = slot
        else:
            if bronz_target_2 == "":
                table_create()
                if choice(0) == 1:
                    slot = choice(1)
                    if "his" in slot:
                        do = """SELECT data FROM gaming_table WHERE slot = '{}'""".format(slot)
                        res = cur.execute(do).fetchall()[0][0]
                        if res != 0:
                            if slot != bronz_target_1:
                                bronz_target_2 = slot
            else:
                pos_1 = int(bronz_target_1[-1])
                pos_2 = int(bronz_target_2[-1])
                do = """SELECT data FROM gaming_table WHERE slot = '{}'""".format(bronz_target_1)
                data_1 = cur.execute(do).fetchall()[0][0]
                do = """SELECT data FROM gaming_table WHERE slot = '{}'""".format(bronz_target_2)
                data_2 = cur.execute(do).fetchall()[0][0]
                wrok_cache[pos_1 - 1], wrok_cache[pos_2 + 3] = wrok_cache[pos_2 + 3], \
                                                                     wrok_cache[pos_1 - 1]
                do = """SELECT ability FROM gaming_table WHERE slot = '{}'""".format(bronz_target_1)
                abil = cur.execute(do).fetchall()[0][0]
                if abil == 1:
                    do = """UPDATE gaming_table SET ability = 1 WHERE slot = '{}'""".format(bronz_target_2)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET ability = 0 WHERE slot = '{}'""".format(bronz_target_1)
                    cur.execute(do)
                do = """SELECT ability FROM gaming_table WHERE slot = '{}'""".format(bronz_target_2)
                abil_2 = cur.execute(do).fetchall()[0][0]
                if abil_2 == 1:
                    do = """UPDATE gaming_table SET ability = 1 WHERE slot = '{}'""".format(bronz_target_1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET ability = 0 WHERE slot = '{}'""".format(bronz_target_2)
                    cur.execute(do)
                if abil_2 == 1 and abil == 1:
                    do = """UPDATE gaming_table SET ability = 1 WHERE slot = '{}'""".format(bronz_target_1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET ability = 1 WHERE slot = '{}'""".format(bronz_target_2)
                    cur.execute(do)
                do = """SELECT health FROM gaming_table WHERE slot = '{}'""".format(bronz_target_1)
                hp_1 = cur.execute(do).fetchall()[0][0]
                do = """SELECT attack FROM gaming_table WHERE slot = '{}'""".format(bronz_target_1)
                att_1 = cur.execute(do).fetchall()[0][0]
                do = """SELECT health FROM gaming_table WHERE slot = '{}'""".format(bronz_target_2)
                hp_2 = cur.execute(do).fetchall()[0][0]
                do = """SELECT attack FROM gaming_table WHERE slot = '{}'""".format(bronz_target_2)
                att_2 = cur.execute(do).fetchall()[0][0]
                update = """UPDATE gaming_table SET data = {} WHERE slot = '{}' """.format(data_2, bronz_target_1)
                cur.execute(update)
                update = """UPDATE gaming_table SET data = {} WHERE slot = '{}' """.format(data_1, bronz_target_2)
                cur.execute(update)
                table_create()
                update = """UPDATE gaming_table SET health = {} WHERE slot = '{}' """.format(hp_2, bronz_target_1)
                cur.execute(update)
                update = """UPDATE gaming_table SET health = {} WHERE slot = '{}' """.format(hp_1, bronz_target_2)
                cur.execute(update)
                update = """UPDATE gaming_table SET attack = {} WHERE slot = '{}' """.format(att_2, bronz_target_1)
                cur.execute(update)
                update = """UPDATE gaming_table SET attack = {} WHERE slot = '{}' """.format(att_1, bronz_target_2)
                cur.execute(update)
                func_choice = 0
                wrok_func()
                bronz_target_1 = ""
                bronz_target_2 = ""
                turn()
    else:
        func_choice = 0
        turn()


def silencer(pos):
    global func_choice
    cch = cache_1[1::2] + cache_2[1::2]
    if cch[0] == 0 and cch[1] == 0 and cch[2] == 0 and cch[3] == 0 and cch[4] == 0 and cch[5] == 0 and cch[6] == 0 \
            and cch[7] == 0:
        func_choice = 0
        do = """UPDATE gaming_table SET health = 0 WHERE slot = 'ur_{}'""".format(pos)
        cur.execute(do)
        pent(pos, 1)
        turn()
    else:
        table_create()
        if choice(0) == 1:
            slot = choice(1)
            do = """SELECT data FROM gaming_table WHERE slot = '{}'""".format(slot)
            res = cur.execute(do).fetchall()[0][0]
            if res != 0:
                do = """SELECT health FROM cards WHERE key = {}""".format(res)
                hp = cur.execute(do).fetchall()[0][0]
                do = """SELECT attack FROM cards WHERE key = {}""".format(res)
                att = cur.execute(do).fetchall()[0][0]
                do = """UPDATE gaming_table SET health = {} WHERE slot = '{}'""".format(hp, slot)
                cur.execute(do)
                do = """UPDATE gaming_table SET attack = {} WHERE slot = '{}'""".format(att, slot)
                cur.execute(do)
                do = """UPDATE gaming_table SET health = 0 WHERE slot = 'ur_{}'""".format(pos)
                cur.execute(do)
                pent(pos, 1)
                death()
                func_choice = 0
                turn()


def pent(pos, side):
    if side == 1:
        start = int(w / 2 - int(w * 0.0065) - 2 * int(w * 0.109)), \
                int(h / 2 - int(h * 0.0039) - int(h * 0.296))
        for z in range(22):
            coord = start[0] + (pos - 1) * (int(w * 0.109) + int(w * 0.0043)), \
                    start[1] + int(h * 0.296) + int(h * 0.296 / 2) - int(w * 0.109 / 2)
            anim = pentagram[z]
            screen.blit(anim, (coord))
            pygame.display.update()
            if z == 10:
                death()
            time.sleep(0.04)
            table_create()


def choice(func):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for i in range(8):
        if click[0] == 1:
            c_s = coord_slots[i]
            if int(c_s[0]) <= int(mouse[0]) <= int(w * 0.109) + int(c_s[0]) and \
                    int(c_s[1]) <= int(mouse[1]) <= int(h * 0.296) + int(c_s[1]):
                if func == 1:
                    if i >= 4:
                        return 'ur_{}'.format(i - 3)
                    else:
                        return 'his_{}'.format(i +1)
                elif func == 0:
                    return 1
    return 0


def fight(enemy, mate):
    start = int(w / 2 - int(w * 0.0065) - 2 * int(w * 0.109)), \
            int(h / 2 - int(h * 0.0039) - int(h * 0.296))
    select_1 = """SELECT data FROM gaming_table WHERE slot = 'his_{}' """.format(enemy)
    select_2 = """SELECT data FROM gaming_table WHERE slot = 'ur_{}' """.format(mate)
    selected_1 = cur.execute(select_1).fetchall()[0][0]
    selected_2 = cur.execute(select_2).fetchall()[0][0]
    table_create()
    if selected_1 != 0 and selected_2 != 0:
        coord_edging = start[0] + (mate - 1) * (int(w * 0.109) + int(w * 0.0043)), start[1] + (int(h * 0.296) + (int(h * 0.0078)))
        d1_at = """SELECT attack FROM gaming_table WHERE slot = 'his_{}' """.format(enemy)
        d1_hp = """SELECT health FROM gaming_table WHERE slot = 'his_{}' """.format(enemy)
        d2_at = """SELECT attack FROM gaming_table WHERE slot = 'ur_{}' """.format(mate)
        d2_hp = """SELECT health FROM gaming_table WHERE slot = 'ur_{}' """.format(mate)
        at1 = cur.execute(d1_at).fetchall()[0][0]
        hp1 = cur.execute(d1_hp).fetchall()[0][0]
        at2 = cur.execute(d2_at).fetchall()[0][0]
        hp2 = cur.execute(d2_hp).fetchall()[0][0]
        if selected_1 == 1 or selected_1 == 2 or selected_1 == 15 or selected_1 == 27:
            at1 *= 2
            at2 *= 2
        if selected_2 == 1 or selected_2 == 2 or selected_2 == 15 or selected_2 == 27:
            at1 *= 2
            at2 *= 2
        pygame.mixer.Sound.play(attack_sound)
        for z in range(15):
            coord = start[0] + (enemy - 1) * (int(w * 0.109) + int(w * 0.0043)), start[1]
            screen.blit(edging, (coord_edging))
            anim = sword_attack[z]
            screen.blit(anim, (coord))
            pygame.display.update()
            time.sleep(0.06)
            table_create()
        if selected_2 == 5:
            if enemy >= 2:
                do = """SELECT health FROM gaming_table WHERE slot = 'his_{}'""".format(enemy - 1)
                res = cur.execute(do).fetchall()[0][0]
                do = """UPDATE gaming_table SET health = {} - {} WHERE slot = 'his_{}'""".format(res, at2, enemy - 1)
                cur.execute(do)
            if enemy <= 3:
                do = """SELECT health FROM gaming_table WHERE slot = 'his_{}'""".format(enemy + 1)
                res = cur.execute(do).fetchall()[0][0]
                do = """UPDATE gaming_table SET health = {} - {} WHERE slot = 'his_{}'""".format(res, at2, enemy + 1)
                cur.execute(do)
        elif selected_2 == 17:
            if enemy >= 2:
                do = """SELECT health FROM gaming_table WHERE slot = 'his_{}'""".format(enemy - 1)
                res = cur.execute(do).fetchall()[0][0]
                do = """UPDATE gaming_table SET health = {} - {} WHERE slot = 'his_{}'""".format(res, at2, enemy - 1)
                cur.execute(do)
            if enemy <= 3:
                do = """SELECT health FROM gaming_table WHERE slot = 'his_{}'""".format(enemy + 1)
                res = cur.execute(do).fetchall()[0][0]
                do = """UPDATE gaming_table SET health = {} - {} WHERE slot = 'his_{}'""".format(res, at2, enemy + 1)
                cur.execute(do)
        if selected_2 != 17:
            hp1 = hp1 - at2
            do_1_hp = """UPDATE gaming_table SET health = {} WHERE slot = 'his_{}' """.format(hp1, enemy)
            cur.execute(do_1_hp)
        table_create()
        coord_edging = start[0] + (enemy - 1) * (int(w * 0.109) + int(w * 0.0043)), start[1]
        screen.blit(edging, (coord_edging))
        pygame.display.update()
        pygame.mixer.Sound.play(attack_sound)
        for z in range(15):
            coord = start[0] + (mate - 1) * (int(w * 0.109) + int(w * 0.0043)), \
                    start[1] + int(h * 0.296) + (int(h * 0.0078))
            screen.blit(edging, (coord_edging))
            table_create()
            screen.blit(edging, (coord_edging))
            anim = sword_attack[z]
            screen.blit(anim, (coord))
            pygame.display.update()
            time.sleep(0.06)
            table_create()
        if selected_1 == 5:
            if mate >= 2:
                do = """SELECT health FROM gaming_table WHERE slot = 'ur_{}'""".format(mate - 1)
                res = cur.execute(do).fetchall()[0][0]
                do = """UPDATE gaming_table SET health = {} - {} WHERE slot = 'ur_{}'""".format(res, at1, mate - 1)
                cur.execute(do)
            if mate <= 3:
                do = """SELECT health FROM gaming_table WHERE slot = 'ur_{}'""".format(mate + 1)
                res = cur.execute(do).fetchall()[0][0]
                do = """UPDATE gaming_table SET health = {} - {} WHERE slot = 'ur_{}'""".format(res, at1, mate + 1)
                cur.execute(do)
        elif selected_1 == 17:
            if mate >= 2:
                do = """SELECT health FROM gaming_table WHERE slot = 'ur_{}'""".format(mate - 1)
                res = cur.execute(do).fetchall()[0][0]
                do = """UPDATE gaming_table SET health = {} - {} WHERE slot = 'ur_{}'""".format(res, at2, mate - 1)
                cur.execute(do)
            if mate <= 3:
                do = """SELECT health FROM gaming_table WHERE slot = 'ur_{}'""".format(mate + 1)
                res = cur.execute(do).fetchall()[0][0]
                do = """UPDATE gaming_table SET health = {} - {} WHERE slot = 'ur_{}'""".format(res, at2, mate + 1)
                cur.execute(do)
        if selected_1 != 17:
            hp2 = hp2 - at1
            do_2_hp = """UPDATE gaming_table SET health = {} WHERE slot = 'ur_{}' """.format(hp2, mate)
            cur.execute(do_2_hp)
        table_create()
        screen.blit(edging, (coord_edging))
        pygame.display.update()
        death()
    elif selected_1 == 0 and selected_2 != 0:
        coord_edging = start[0] + (mate - 1) * (int(w * 0.109) + int(w * 0.0043)), start[1] + (int(h * 0.296) + (int(h * 0.0078)))
        screen.blit(edging, (coord_edging))
        pygame.display.update()
        time.sleep(0.5)
        d2_at = """SELECT attack FROM gaming_table WHERE slot = 'ur_{}' """.format(mate)
        at2 = cur.execute(d2_at).fetchall()[0][0]
        p_at2 = """SELECT data FROM gaming_table WHERE slot = 'ur_at' """
        pers_at2 = cur.execute(p_at2).fetchall()[0][0]
        pers_at2 += at2
        update = """UPDATE gaming_table SET data = {} WHERE slot = 'ur_at' """.format(pers_at2)
        cur.execute(update)
    elif selected_1 != 0 and selected_2 == 0:
        coord_edging = start[0] + (enemy - 1) * (int(w * 0.109) + int(w * 0.0043)), start[1]
        screen.blit(edging, (coord_edging))
        pygame.display.update()
        time.sleep(0.5)
        d1_at = """SELECT attack FROM gaming_table WHERE slot = 'his_{}' """.format(enemy)
        at1 = cur.execute(d1_at).fetchall()[0][0]
        p_at1 = """SELECT data FROM gaming_table WHERE slot = 'his_at' """
        pers_at1 = cur.execute(p_at1).fetchall()[0][0]
        pers_at1 += at1
        update = """UPDATE gaming_table SET data = {} WHERE slot = 'his_at' """.format(pers_at1)
        cur.execute(update)


def death():
    global death_cache_1, death_cache_2
    wrok_func()
    for ind in range(4):
        select_1 = """SELECT data FROM gaming_table WHERE slot = 'his_{}' """.format(ind + 1)
        select_2 = """SELECT data FROM gaming_table WHERE slot = 'ur_{}' """.format(ind + 1)
        selected_1 = cur.execute(select_1).fetchall()[0][0]
        selected_2 = cur.execute(select_2).fetchall()[0][0]
        do = """SELECT health FROM gaming_table WHERE slot = 'his_{}' """.format(ind + 1)
        hp1 = cur.execute(do).fetchall()[0][0]
        do = """SELECT health FROM gaming_table WHERE slot = 'ur_{}' """.format(ind + 1)
        hp2 = cur.execute(do).fetchall()[0][0]
        if selected_1 != 0:
            if hp1 <= 0:
                do_1 = """UPDATE gaming_table SET data = 0 WHERE slot = 'his_{}' """.format(ind + 1)
                cur.execute(do_1)
                do_1 = """UPDATE gaming_table SET ability = 0 WHERE slot = 'his_{}' """.format(ind + 1)
                cur.execute(do_1)
                do_1 = """UPDATE gaming_table SET attack = 0 WHERE slot = 'his_{}' """.format(ind + 1)
                cur.execute(do_1)
                death_cache_1[ind] = 1
                if selected_1 == 9:
                    do = """UPDATE gaming_table SET data = 26 WHERE slot = 'his_{}'""".format(ind+1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET health = 3 WHERE slot = 'his_{}'""".format(ind + 1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET attack = 2 WHERE slot = 'his_{}'""".format(ind + 1)
                    cur.execute(do)
                elif selected_1 == 10:
                    do = """UPDATE gaming_table SET data = 27 WHERE slot = 'his_{}'""".format(ind + 1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET health = 2 WHERE slot = 'his_{}'""".format(ind + 1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET attack = 2 WHERE slot = 'his_{}'""".format(ind + 1)
                    cur.execute(do)
        if selected_2 != 0:
            if hp2 <= 0:
                do_2 = """UPDATE gaming_table SET data = 0 WHERE slot = 'ur_{}' """.format(ind + 1)
                cur.execute(do_2)
                do_2 = """UPDATE gaming_table SET ability = 0 WHERE slot = 'ur_{}' """.format(ind + 1)
                cur.execute(do_2)
                do_2 = """UPDATE gaming_table SET attack = 0 WHERE slot = 'ur_{}' """.format(ind + 1)
                cur.execute(do_2)
                death_cache_2[ind] = 1
                if selected_2 == 9:
                    do = """UPDATE gaming_table SET data = 26 WHERE slot = 'ur_{}'""".format(ind + 1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET health = 3 WHERE slot = 'ur_{}'""".format(ind + 1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET attack = 2 WHERE slot = 'ur_{}'""".format(ind + 1)
                    cur.execute(do)
                if selected_2 == 10:
                    do = """UPDATE gaming_table SET data = 27 WHERE slot = 'ur_{}'""".format(ind + 1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET health = 2 WHERE slot = 'ur_{}'""".format(ind + 1)
                    cur.execute(do)
                    do = """UPDATE gaming_table SET attack = 2 WHERE slot = 'ur_{}'""".format(ind + 1)
                    cur.execute(do)
    death_anim()


def death_anim():
    global death_cache_1, death_cache_2, death_coord_1, death_coord_2
    scale = 1
    start = int(w / 2 - int(w * 0.0065) - 2 * int(w * 0.109)), \
            int(h / 2 - int(h * 0.0039) - int(h * 0.296))
    while scale > 0:
        coords = int(w * 0.109 * (1 - scale) / 2), int(h * 0.296 * (1 - scale) / 2)
        for ind in range(4):
            if death_cache_1[ind] == 1:
                cache_1[ind * 2] = pygame.transform.scale(cache_1[ind * 2], (int(w * 0.109 * scale), int(h * 0.296 * scale)))
                coord = [start[0] + ind * (int(w * 0.109) + int(w * 0.0043)) + coords[0], start[1] + coords[1]]
                death_coord_1[ind] = coord
        for ind in range(4):
            if death_cache_2[ind] == 1:
                cache_2[ind * 2] = pygame.transform.scale(cache_2[ind * 2], (int(w * 0.109 * scale), int(h * 0.296 * scale)))
                coord = [start[0] + ind * (int(w * 0.109) + int(w * 0.0043)) + coords[0], start[1] + int(h * 0.296) + int(h * 0.0078) + coords[1]]
                death_coord_2[ind] = coord
        scale -= 0.05
        table_create()
        pygame.display.update()
    for i in range(len(death_cache_1)):
        if death_cache_1[i] == 1:
            cache_1[i * 2 + 1] = 0
    for i in range(len(death_cache_2)):
        if death_cache_2[i] == 1:
            cache_2[i * 2 + 1] = 0
    death_cache_1 = [0, 0, 0, 0]
    death_cache_2 = [0, 0, 0, 0]


def run_menu():
    pymixer.set_volume(0.5)
    screen.blit(bg, (0, 0))
    screen.blit(menu_plate, (w // 2 - int(w * 0.292) // 2, h // 2 - int(h * 0.687) // 2))
    game = True
    button_start = Button(int(w * 0.131), int(h * 0.065), w // 2 - int(w * 0.065), h * 0.3, "В бой!", w * 0.478, h * 0.321, int(text_size * 1.05))
    button_exit = Button(int(w * 0.131), int(h * 0.065), w // 2 - int(w * 0.065), h * 0.6, "Акоп", w * 0.485, h * 0.621, text_size)
    button_settings = Button(int(w * 0.131), int(h * 0.065), w // 2 - int(w * 0.065), h * 0.45, "Настройки", w * 0.462, h * 0.471, text_size)
    button_inventory = SettingsButton(w // 2 - int(w * 0.023), h * 0.7445, w // 2 - int(w * 0.023) + int(h * 0.1), h * 0.7445 + int(h * 0.09))
    while game:
        button_inventory.open_lootbox()
        button_exit.draw_close()
        button_start.draw_start()
        button_settings.draw_settings()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_menu()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()


def run_settings():
    button = Button(int(w * 0.021), int(h * 0.039), w - int(w * 0.021), 0, "X", w - int(w * 0.016), int(h * 0.0117), text_size)
    change_music = SettingsButton(int(w * 0.141), int(h * 0.488), int(w * 0.511), int(h * 0.565))
    change_volume = SettingsButton(int(w * 0.258), int(h * 0.23), int(w * 0.568), int(h * 0.415))
    game = True
    while game:
        screen.blit(settings_bg, (0, 0))
        screen.blit(volume_bar[volume_index], (int(w * 0.258), int(h * 0.23)))
        print_text("Громкость звука", int(w * 0.07), int(h * 0.29), int(text_size * 1.6), (200, 200, 200))
        print_text('Кликните на название, чтобы изменить музыку', int(w * 0.07), int(h * 0.43), int(text_size * 1.25), (200, 200, 200))
        print_text('Играет:', int(w * 0.07), int(h * 0.51), int(text_size * 1.25), (200, 200, 200))
        print_text(bg_music_index[index], int(w * 0.15), int(h * 0.51), int(text_size * 1.25), (200, 200, 200))
        button.draw_back()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                change_volume.volume_change()
                change_music.music_change()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

def run_lootbox():
    global drop
    game = True
    button = Button(int(w * 0.021), int(h * 0.039), w - int(w * 0.021), 0, "X", w - int(w * 0.016), int(h * 0.0117),
                    text_size)
    open_button = Button(int(w * 0.09), int(h * 0.055), int(w // 2) - int(w * 0.045), int(h * 0.9), "100 Монет", int(w // 2) - int(w * 0.035), int(h * 0.919),
                    text_size)
    while game:
        do = """SELECT data FROM inventory WHERE name = 'money'"""
        coins = cur.execute(do).fetchall()[0][0]
        money = Button(int(w * 0.04), int(h * 0.04), w - int(w * 0.045), int(h * 0.958),
                       "Ваши монеты:   {}".format(coins), w - int(w * 0.15), int(h * 0.97),
                       text_size, font_color=(255, 255, 255))
        screen.blit(bg, (0, 0))
        screen.blit(pygame.transform.scale(tupo_pent, (int(h * 0.7), int(h * 0.7))), (int(w // 2) - int(h * 0.7 * 0.5), int(h // 2) - int(h * 0.7 * 0.5)))
        pygame.draw.rect(screen, "white", (int(w // 2) - int(w * 0.109 * 0.5) - 5, int(h // 2) - int(h * 0.47) - 5, int(w * 0.109) + 10, int(h * 0.296) + 10))
        screen.blit(pygame.transform.scale(bestiary, (int(w * 0.109), int(h * 0.296))), (int(w // 2) - int(w * 0.109 * 0.5), int(h // 2) - int(h * 0.47)))
        if drop != []:
            if drop[0] != 0:
                coord_x = int(w // 2) - int(w * 0.109 * 0.5)
                coord_y = int(h // 2) - int(h * 0.47)
                dop_x = 20 * int(w * 0.17 / 21)
                dop_y = 20 * int(h * 0.255 / 21)
                dop_x_2 = 20 * int(w * 0.118 / 21)
                dop_y_2 = 20 * int(h * 0.625 / 21)
                shirina = int(w * 0.109)
                visota = int(h * 0.296)
                print(visota)
                screen.blit(drop[1], (coord_x - dop_x,
                                      coord_y + dop_y))
                screen.blit(drop[3], (coord_x + dop_x,
                                      coord_y + dop_y))
                screen.blit(drop[5], (coord_x - dop_x_2,
                                      coord_y + dop_y_2))
                screen.blit(drop[7], (coord_x + dop_x_2,
                                      coord_y + dop_y_2))
                coord = pygame.mouse.get_pos()
                if coord_x - dop_x <= coord[0] <= coord_x - dop_x + shirina:
                    if coord_y + dop_y <= coord[1] <= coord_y + dop_y + visota:
                        do = """SELECT name FROM cards WHERE key = {}""".format(drop[0])
                        result = cur.execute(do).fetchall()[0][0]
                        card_show = pygame.image.load("{}_stats.png".format(result))
                        card_show = pygame.transform.scale(card_show, (int(w * 0.101) * 2.5, int(h * 0.278) * 2.5))
                        screen.blit(card_show, (0, h / 2 - int(h * 0.278) * 1.25))
                elif coord_x + dop_x <= coord[0] <= coord_x + dop_x + shirina:
                    if coord_y + dop_y <= coord[1] <= coord_y + dop_y + visota:
                        do = """SELECT name FROM cards WHERE key = {}""".format(drop[2])
                        result = cur.execute(do).fetchall()[0][0]
                        card_show = pygame.image.load("{}_stats.png".format(result))
                        card_show = pygame.transform.scale(card_show, (int(w * 0.101) * 2.5, int(h * 0.278) * 2.5))
                        screen.blit(card_show, (0, h / 2 - int(h * 0.278) * 1.25))
                if coord_x - dop_x_2 <= coord[0] <= coord_x - dop_x_2 + shirina:
                    if coord_y + dop_y_2 <= coord[1] <= coord_y + dop_y_2 + visota:
                        do = """SELECT name FROM cards WHERE key = {}""".format(drop[4])
                        result = cur.execute(do).fetchall()[0][0]
                        card_show = pygame.image.load("{}_stats.png".format(result))
                        card_show = pygame.transform.scale(card_show, (int(w * 0.101) * 2.5, int(h * 0.278) * 2.5))
                        screen.blit(card_show, (0, h / 2 - int(h * 0.278) * 1.25))
                elif coord_x + dop_x_2 <= coord[0] <= coord_x + dop_x_2 + shirina:
                    if coord_y + dop_y_2 <= coord[1] <= coord_y + dop_y_2 + visota:
                        do = """SELECT name FROM cards WHERE key = {}""".format(drop[6])
                        result = cur.execute(do).fetchall()[0][0]
                        card_show = pygame.image.load("{}_stats.png".format(result))
                        card_show = pygame.transform.scale(card_show, (int(w * 0.101) * 2.5, int(h * 0.278) * 2.5))
                        screen.blit(card_show, (0, h / 2 - int(h * 0.278) * 1.25))
        mouse = pygame.mouse.get_pressed()
        if mouse[0] == 1:
            drop = []
        button.draw_back()
        open_button.opening_lootbox()
        money.otrisovka()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_menu()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()


def run_game():
    global pos_abil, func_choice
    game = True
    while game:
        if func_choice == 0:
            table_create()
            button = Button(int(w * 0.044), int(h * 0.039), w - int(w * 0.044), int(h / 2) - int(h * 0.039),
                            "Turn", w - int(w * 0.036), int(h / 2) - int(h * 0.028), text_size)
            button.draw_turn()
            button = Button(int(w * 0.022), int(h * 0.039), w - int(w * 0.022), 0, "X", w - int(w * 0.016), int(h * 0.011), text_size)
            button.draw_back()
            table_active()
        elif func_choice == 2:
            daw_func()
        elif func_choice == 3:
            solar_func(pos_abil)
        elif func_choice == 13:
            demilich_func()
        elif func_choice == 16:
            wrok_func()
            turn()
        elif func_choice == 19:
            shadow_demon(pos_abil)
        elif func_choice == 24:
            bronz_dragon()
        elif func_choice == 28:
            silencer(pos_abil)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_menu()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()


run_menu()

