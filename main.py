import csv
import sys
import os
import pygame
import spritesheet
import random


clock = pygame.time.Clock()
# set game FPS
FPS = 60

end_count = 0

pygame.init()
screen = pygame.display.set_mode((1280, 960))


def file_load(file_name):
    file_scan = []
    with open(f"Levels\\{file_name}.csv", newline="") as csvfile:
        mapreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in mapreader:
            file_scan.append(row[0].split(","))

    for i in range(len(file_scan)):
        for o in range(len(file_scan[i])):
            file_scan[i][o] = int(file_scan[i][o])

    return file_scan


levels = [file_load("level1"), file_load("level2"),file_load("level3")]

world_map = levels[0]

running = True

player_x = int(world_map[-1][0])
player_y = int(world_map[-1][1])
direction = "r"

state = "idle"
game_state = "start"

background_img = pygame.image.load("assets\\background.png").convert()

player_spritesheet = spritesheet.SpriteSheet("assets\\player_spritesheet.png")

tilemap = spritesheet.SpriteSheet("assets\\tilemap.png")
tilemap = tilemap.images_at(((0,0,0,0),(192,192,64,64),(64,64,64,64),(192,64,64,64),(192,128,64,64),(128,192,64,64),(192,0,64,64),(0,128,64,64),(128,128,64,64),(0,0,64,64),(128,0,64,64),
                             (128,64,64,64),(0,64,64,64),(64,0,64,64),(64,128,64,64),(0,192,64,64),(64,192,64,64)))

spike = pygame.image.load("assets\\spike.png").convert_alpha()
flag = pygame.image.load("assets\\flag.png").convert_alpha()
spring = pygame.image.load("assets\\spring.png").convert_alpha()

croc_spritesheet_l = spritesheet.SpriteSheet("assets\\crocs_spritesheet_l.png")
croc_spritesheet_l = croc_spritesheet_l.images_at(((0,0,64,96),(64,0,64,96),(128,0,64,96),(192,0,64,96),(256,0,64,96),(320,0,64,96),(384,0,64,96),(448,0,64,96),(512,0,64,96),(576,0,64,96),(640,0,64,96),(704,0,64,96),(768,0,64,96)), colorkey=(0,0,0))

croc_spritesheet_r = spritesheet.SpriteSheet("assets\\crocs_spritesheet_r.png")
croc_spritesheet_r = croc_spritesheet_r.images_at(((0,0,64,96),(64,0,64,96),(128,0,64,96),(192,0,64,96),(256,0,64,96),(320,0,64,96),(384,0,64,96),(448,0,64,96),(512,0,64,96),(576,0,64,96),(640,0,64,96),(704,0,64,96),(768,0,64,96)), colorkey=(0,0,0))

ost = pygame.mixer.Sound("assets\\Platformy OST.mp3")
blank_sound = pygame.mixer.Sound("assets\\1-second-of-silence.mp3")
fail = pygame.mixer.Sound("assets\\fail.mp3")

x_velocity = 0
y_velocity = 0

max_x_velocity = 5
max_y_up_velocity = 10
max_y_down_velocity = 20

jumpspeed = 0.25
gravity_fall = 0.5
x_acceleration = 0.5
start_jump = 0

# sprite stages
idle_sprite = 1
left_sprite = 1
right_sprite = 1

# start screen
title_y = 0
start_option_selected = 0

#end_option_selected
end_option = 0

#pause option selected
pause_option = 0

#for controls and options menu
screen_to_return_to = "start"

time = [0,0,0]
start_time = [0,0,0]
end_time = [0,0,0]

#settings
option_selected = 0
difficulty_val = 2
difficulty_stages = ["Baby","Easy","Normal"]
music_val = 0
music_stages = ["on","off"]
sfx_val = 0
sfx_stages = ["on","off"]
timer_val = 0
timer_stages = ["on","off"]
screen_size_val = 1
screen_size_stages = ["small","medium","large"]

# length of cyote(frames)
coyote_time = 5
##update cyote
coyote = coyote_time

#music
playing_music = False
play_music = pygame.USEREVENT + 1
chanel = pygame.mixer.Channel(0)

#follower
start_moving = False
past_coord = []
croc_num = 0
croc_time = 61

#screen refresh
resolution_scale = 1

#fail comments
spike_fail_comments = ["Didn't you see that","Ouch","Sharp","Pointy","That's not good","You made a mess","don't jump there","git gud","that was pointy","Spike 1, You 0","it had a point","Did you want a hug?"]
croc_fail_comments = ["I'm sure you're tasty","Ouch","nom nom nom","You're supposed to run","really?","How do teeth feel?","was that fun?","git gud","player-flavoured","bite-sized performance","jaws of defeat"]
fail_comment_size = 0
fail_comment = ""

pause_start_time = 0
buffer_time = 0


def show_text(text, font_size, colour, centre_coords):
    txt = pygame.font.Font("PressStart2P.ttf", int(font_size*resolution_scale)).render(text, True, colour)
    txt_rect = txt.get_rect()
    txt_rect.center = (centre_coords[0]*resolution_scale,centre_coords[1]*resolution_scale)
    screen.blit(txt, txt_rect)


def level_reset():
    global player_x, player_y, game_state, x_velocity, y_velocity, start_moving, past_coord,start_time, buffer_time

    start_moving = False
    start_time[levels.index(world_map)] = 0
    past_coord = []

    player_x = int(world_map[-1][0])
    player_y = int(world_map[-1][1])

    x_velocity = 0
    y_velocity = 0

    game_state = "level"

    buffer_time = 0


def restart():
    level_reset()

    if sfx_val == 0:
        pygame.mixer.Sound.play(fail, 0)


def get_sprite():
    global img, left_sprite, right_sprite, idle_sprite

    if state == "idle" and direction == "r":
        if 1 <= idle_sprite <= 100:
            img = player_spritesheet.image_at((128,0,64,96),colorkey=(0,0,0))
            idle_sprite += 1
        elif 101 <= idle_sprite <= 200:
            img = player_spritesheet.image_at((192,0,64,96),colorkey=(0,0,0))
            idle_sprite += 1
        else:
            idle_sprite = 1

    if state == "idle" and direction == "l":
        if 1 <= idle_sprite <= 100:
            img = player_spritesheet.image_at((0,0,64,96),colorkey=(0,0,0))
            idle_sprite += 1
        elif 101 <= idle_sprite <= 200:
            img = player_spritesheet.image_at((64,0,64,96),colorkey=(0,0,0))
            idle_sprite += 1
        else:
            idle_sprite = 1

    if state == "run" and direction == "r":
        if 1 <= right_sprite <= 10:
            img = player_spritesheet.image_at((512,0,64,96),colorkey=(0,0,0))
            right_sprite += 1
        elif 11 <= right_sprite <= 20:
            img = player_spritesheet.image_at((576,0,64,96),colorkey=(0,0,0))
            right_sprite += 1
        elif 21 <= right_sprite <= 30:
            img = player_spritesheet.image_at((640,0,64,96),colorkey=(0,0,0))
            right_sprite += 1
        elif 31 <= right_sprite <= 40:
            img = player_spritesheet.image_at((704,0,64,96),colorkey=(0,0,0))
            right_sprite += 1
        else:
            right_sprite = 1

    if state == "run" and direction == "l":
        if 1 <= left_sprite <= 10:
            img = player_spritesheet.image_at((256,0,64,96),colorkey=(0,0,0))
            left_sprite += 1
        elif 11 <= left_sprite <= 20:
            img = player_spritesheet.image_at((320,0,64,96),colorkey=(0,0,0))
            left_sprite += 1
        elif 21 <= left_sprite <= 30:
            img = player_spritesheet.image_at((384,0,64,96),colorkey=(0,0,0))
            left_sprite += 1
        elif 31 <= left_sprite <= 40:
            img = player_spritesheet.image_at((448,0,64,96),colorkey=(0,0,0))
            left_sprite += 1
        else:
            left_sprite = 1

    if state == "jump_up":
        if direction == "l":
            img = player_spritesheet.image_at((768,0,64,96),colorkey=(0,0,0))
        else:
            img = player_spritesheet.image_at((832,0,64,96),colorkey=(0,0,0))

    if state == "fall":
        if direction == "l":
            img = player_spritesheet.image_at((896,0,64,96),colorkey=(0,0,0))
        else:
            img = player_spritesheet.image_at((960,0,64,96),colorkey=(0,0,0))


def draw_tile(image, x, y):
    screen.blit(image, (x*resolution_scale,y*resolution_scale))


def generate_fail_comment(list):
    global fail_comment_size, fail_comment

    fail_comment = random.choice(list)
    fail_comment_size = 30


def draw_level(world_map):
    global player,past_coord, croc_num, time_shown, img, fail_comment_size

    get_sprite()
    draw_tile(background_img, 0, 0)

    player_offset = player_x % 64 + 32
    player_bit = (player_x // 64) - 9.5

    # tile map
    for y in range(15):
        for x in range(22):
            if player_x < 608:
                tile = world_map[y][x]
                player_offset = 0
            elif player_x > len(world_map[0]) * 64 - 736:
                player_offset = 0
                if x > 19:
                    continue
                tile = world_map[y][int(x + (len(world_map[0]) - 21))]
            else:
                tile = world_map[y][int(player_bit + x)]
            # spike
            if tile == -1:
                draw_tile(spike,x * 64 - player_offset, y * 64)
            # #spring
            elif tile == 99:
                draw_tile(spring,x * 64 - player_offset, y * 64)
            #flag
            elif tile == -99:
                draw_tile(flag,x * 64 - player_offset, y * 64)
            else:
                draw_tile(tilemap[tile],x * 64 - player_offset, y * 64)

    img = pygame.transform.scale(img, (64*resolution_scale,96*resolution_scale))
    if player_x < 608:
        draw_tile(img, player_x, player_y)
    elif player_x > len(world_map[0]) * 64 - 736:
        draw_tile(img, (1346 - (len(world_map[0]) * 64 - player_x)), player_y)
    else:
        draw_tile(img, 608, player_y)

    if len(past_coord) > croc_time:
        croc_num += 1

        if past_coord[0][2] == "r":
            croc = croc_spritesheet_r[croc_num//6]
        else:
            croc = croc_spritesheet_l[croc_num // 6]
        if croc_num == 66:
            croc_num = 0
        croc = pygame.transform.scale(croc,(64*resolution_scale,96*resolution_scale))

        if player_x < 608:
            screen.blit(croc, (past_coord[0][0]*resolution_scale,past_coord[0][1]*resolution_scale))
        elif player_x > len(world_map[0]) * 64 - 736:
            screen.blit(croc, ((1346 - (len(world_map[0]) * 64 - past_coord[0][0]))*resolution_scale, past_coord[0][1]*resolution_scale))
        else:
            screen.blit(croc, ((608-(player_x-past_coord[0][0]))*resolution_scale,past_coord[0][1]*resolution_scale))

        past_coord.pop(0)

    if timer_val == 0:

        if start_moving:
            if game_state == "level":
                time_shown = str(pygame.time.get_ticks()-start_time[levels.index(world_map)]-buffer_time)
            elif game_state == "pause":
                time_shown = str(pause_start_time-start_time[levels.index(world_map)]-buffer_time)
        else:
            time_shown = "0000"

        if len(time_shown) < 4:
            time_shown = "0." + time_shown
        else:
            time_shown = time_shown[0:-3] + "." + time_shown[-4:-1]
        pygame.draw.rect(screen, (255, 255, 255), (20*resolution_scale, 50*resolution_scale, (250 + (len(time_shown)-5)*50)*resolution_scale, 50*resolution_scale))
        show_text(time_shown, 48,(0,0,0),((120 + (len(time_shown)-4)*25),80))

    if fail_comment_size != 0:
        show_text(fail_comment, fail_comment_size,(255,0,0),(world_map[-1][0]+32,world_map[-1][1]-32))
        fail_comment_size -= 0.5


def refresh_settings():
    global croc_time, resolution_scale, tilemap,screen,spring,spike,flag

    if difficulty_val == 0:
        croc_time = 10000000000
    elif difficulty_val == 1:
        croc_time = 120
    else:
        croc_time = 61

    if screen_size_val == 0:
        resolution_scale = 0.5
    elif screen_size_val == 1:
        resolution_scale = 0.75
    else:
        resolution_scale = 1

    new_tilemap = [tilemap[0]]
    for tiles in tilemap:
        if tilemap.index(tiles) != 0:
            new_tilemap.append(pygame.transform.scale(tiles, (64 * resolution_scale, 64 * resolution_scale)))
    tilemap = new_tilemap
    spring = pygame.transform.scale(spring, (64 * resolution_scale, 64 * resolution_scale))
    spike = pygame.transform.scale(spike, (64 * resolution_scale, 64 * resolution_scale))
    flag = pygame.transform.scale(flag, (64 * resolution_scale, 64 * resolution_scale))
    pygame.transform.scale(background_img, (1280 * resolution_scale, 960 * resolution_scale))
    screen = pygame.display.set_mode((1280*resolution_scale, 960*resolution_scale))


def draw_start_menu():
    global title_y

    screen.fill((144, 255, 189))

    show_text("PLATFORMY",96,(255, 189, 144),(640, title_y))

    if start_option_selected == 0:
        play_prompt_colour = (255, 189, 144)
    else:
        play_prompt_colour = (0,0,0)

    if start_option_selected == 1:
        controls_prompt_colour = (255, 189, 144)
    else:
        controls_prompt_colour = (0,0,0)

    if start_option_selected == 2:
        options_prompt_colour = (255, 189, 144)
    else:
        options_prompt_colour = (0,0,0)

    if start_option_selected == 3:
        quit_prompt_colour = (255, 189, 144)
    else:
        quit_prompt_colour = (0,0,0)

    if title_y != 128:
        title_y += 2

    if title_y == 128:
        show_text("PLAY", 48, play_prompt_colour, (640, 360))
        show_text("CONTROLS",48,controls_prompt_colour,(640,460))
        show_text("OPTIONS",48,options_prompt_colour,(640,560))
        show_text("QUIT",48,quit_prompt_colour,(640,660))

        pygame.draw.circle(screen, (255, 189, 144), (400*resolution_scale, (360 + 100 * start_option_selected)*resolution_scale), 16*resolution_scale)
        pygame.draw.circle(screen, (255, 189, 144), (880*resolution_scale, (360 + 100 * start_option_selected)*resolution_scale), 16*resolution_scale)
        pygame.draw.polygon(screen, (255, 189, 144),[[375*resolution_scale,(360 + 100 * start_option_selected)*resolution_scale],
                                                     [330*resolution_scale,(330 + 100 * start_option_selected)*resolution_scale],
                                                     [330*resolution_scale,(390 + 100 * start_option_selected)*resolution_scale]])
        pygame.draw.polygon(screen, (255, 189, 144),[[905*resolution_scale, (360 + 100 * start_option_selected)*resolution_scale],
                                                     [960*resolution_scale, (330 + 100 * start_option_selected)*resolution_scale],
                                                     [960*resolution_scale, (390 + 100 * start_option_selected)*resolution_scale]])


def draw_end_screen():
    screen.fill((255, 181, 68))

    show_text("VICTORY",96,(68, 142, 255),(640,256))

    if end_count > 3:
        show_text("Stage 1", 48, (68, 142, 255), (280,380))
        show_text(str(time[0]), 48, (68, 142, 255), (640,380))
        show_text("Stage 2", 48, (68, 142, 255), (280, 480))
        show_text(str(time[1]), 48, (68, 142, 255), (640, 480))
        show_text("Stage 3", 48, (68, 142, 255), (280, 580))
        show_text(str(time[2]), 48, (68, 142, 255), (640, 580))
        pygame.draw.line(screen, (68,142,255),(80*resolution_scale,620*resolution_scale),(1200*resolution_scale,620*resolution_scale))
        if end_option == 0:
            play_again_col = (68,142,255)
        else:
            play_again_col = (185, 213, 255)
        show_text("PLAY AGAIN",48, play_again_col, (640,680))
        if end_option == 1:
            exit_col = (68,142,255)
        else:
            exit_col = (185, 213, 255)
        show_text("EXIT",48, exit_col, (640,780))
        pygame.draw.circle(screen,(68,142,255),(320*resolution_scale,(680+100*end_option)*resolution_scale),16*resolution_scale)
        pygame.draw.circle(screen, (68, 142, 255),(960 * resolution_scale, (680 + 100 * end_option) * resolution_scale), 16 * resolution_scale)
        pygame.draw.polygon(screen,(68,142,255), [[300*resolution_scale,(680+100*end_option)*resolution_scale],
                                                  [270*resolution_scale,(650+100*end_option)*resolution_scale],
                                                  [270*resolution_scale,(710+100*end_option)*resolution_scale]])
        pygame.draw.polygon(screen, (68, 142, 255),
                            [[980 * resolution_scale, (680 + 100 * end_option) * resolution_scale],
                             [1010 * resolution_scale, (650 + 100 * end_option) * resolution_scale],
                             [1010 * resolution_scale, (710 + 100 * end_option) * resolution_scale]])


def draw_pause_menu():
    draw_level(world_map)

    pygame.draw.rect(screen, (43, 178, 192), (320*resolution_scale, 0*resolution_scale, 640*resolution_scale, 1280*resolution_scale))
    show_text("PAUSE",96,(192, 57, 43),(640,256))

    if pause_option == 0:
        resume_colour = (192, 57, 43)
    else:
        resume_colour = (239,206,202)
    show_text("RESUME",48,resume_colour,(640,360))

    if pause_option == 1:
        controls_colour = (192, 57, 43)
    else:
        controls_colour = (239,206,202)
    show_text("CONTROLS",48,controls_colour,(640,460))

    if pause_option == 2:
        options_colour = (192, 57, 43)
    else:
        options_colour = (239,206,202)
    show_text("OPTIONS",48,options_colour,(640,560))

    if pause_option == 3:
        exit_colour = (192, 57, 43)
    else:
        exit_colour = (239,206,202)
    show_text("EXIT",48,exit_colour,(640,660))

    pygame.draw.circle(screen, (192, 57, 43), (430 * resolution_scale, (360 + 100 * pause_option) * resolution_scale),
                       16 * resolution_scale)
    pygame.draw.circle(screen, (192, 57, 43), (850 * resolution_scale, (360 + 100 * pause_option) * resolution_scale),
                       16 * resolution_scale)
    pygame.draw.polygon(screen, (192, 57, 43), [[410 * resolution_scale, (360 + 100 * pause_option) * resolution_scale],
                                                 [380 * resolution_scale, (330 + 100 * pause_option) * resolution_scale],
                                                 [380 * resolution_scale, (390 + 100 * pause_option) * resolution_scale]])
    pygame.draw.polygon(screen, (192, 57, 43),
                        [[870 * resolution_scale, (360 + 100 * pause_option) * resolution_scale],
                         [900 * resolution_scale, (330 + 100 * pause_option) * resolution_scale],
                         [900 * resolution_scale, (390 + 100 * pause_option) * resolution_scale]])


def draw_controls_menu():
    screen.fill((144, 255, 189))

    show_text("CONTROLS", 72, (255, 189, 144), (640, 80))

    show_text("Move left and right",32,(255, 189, 144),(960,220))

    pygame.draw.rect(screen, (189, 195, 199), (50*resolution_scale, 190*resolution_scale, 55*resolution_scale, 55*resolution_scale))
    show_text("A",48,(0,0,0),(80,220))

    pygame.draw.rect(screen, (189, 195, 199), (150*resolution_scale, 190*resolution_scale, 55*resolution_scale, 55*resolution_scale))
    show_text("D", 48, (0, 0, 0), (180, 220))

    show_text("or", 32, (0, 0, 0), (320, 220))

    pygame.draw.rect(screen, (189, 195, 199), (430*resolution_scale, 190*resolution_scale, 55*resolution_scale, 55*resolution_scale))
    show_text("←", 48, (0, 0, 0), (460, 220))

    pygame.draw.rect(screen, (189, 195, 199), (530*resolution_scale, 190*resolution_scale, 55*resolution_scale, 55*resolution_scale))
    show_text("→", 48, (0, 0, 0), (560, 220))

    #jump controls
    show_text("Jump",32,(255,189,144),(960,320))

    pygame.draw.rect(screen, (189, 195, 199), (50*resolution_scale, 290*resolution_scale, 55*resolution_scale, 55*resolution_scale))
    show_text("W",48,(0,0,0),(80,320))

    show_text("or", 32, (0, 0, 0), (200, 320))

    pygame.draw.rect(screen, (189, 195, 199), (290*resolution_scale, 290*resolution_scale, 55*resolution_scale, 55*resolution_scale))
    show_text("↑", 48, (0, 0, 0), (320, 320))

    show_text("or", 40, (0, 0, 0), (440, 320))

    pygame.draw.rect(screen, (189, 195, 199), (520*resolution_scale, 290*resolution_scale, 240*resolution_scale, 55*resolution_scale))
    show_text("SPACE",48,(0,0,0),(640,320))

    #Pause or leave menus
    show_text("Pause game or leave menus", 32, (255, 189, 144), (840, 420))

    pygame.draw.rect(screen, (189, 195, 199), (240*resolution_scale, 390*resolution_scale, 150*resolution_scale, 55*resolution_scale))
    show_text("ESC", 48, (0, 0, 0), (320, 420))

    #restart level
    show_text("restart a level", 32, (255, 189, 144), (960, 520))

    pygame.draw.rect(screen, (189, 195, 199), (190*resolution_scale, 490*resolution_scale, 250*resolution_scale, 55*resolution_scale))
    show_text("ENTER", 48, (0, 0, 0), (320, 520))

    #menu navigation
    show_text("move around menus", 32, (255, 189, 144), (960, 620))

    pygame.draw.rect(screen, (189, 195, 199), (150*resolution_scale, 570*resolution_scale, 55*resolution_scale, 55*resolution_scale))
    show_text("W", 48, (0, 0, 0), (180, 600))
    pygame.draw.rect(screen, (189, 195, 199), (150*resolution_scale, 640*resolution_scale, 55*resolution_scale, 55*resolution_scale))
    show_text("S", 48, (0, 0, 0), (180, 670))

    show_text("or", 40, (0, 0, 0), (320, 620))

    pygame.draw.rect(screen, (189, 195, 199), (430*resolution_scale, 570*resolution_scale, 55*resolution_scale, 55*resolution_scale))
    show_text("↑", 48, (0, 0, 0), (460, 600))
    pygame.draw.rect(screen, (189, 195, 199), (430*resolution_scale, 640*resolution_scale, 55*resolution_scale, 55*resolution_scale))
    show_text("↓", 48, (0, 0, 0), (460, 670))

    #select in menus
    show_text("Select in menus", 32, (255, 189, 144), (960, 750))
    pygame.draw.rect(screen, (189, 195, 199), (40*resolution_scale, 720*resolution_scale, 240*resolution_scale, 55*resolution_scale))
    show_text("SPACE", 48, (0, 0, 0), (160, 750))
    show_text("or", 40, (0, 0, 0), (360, 750))
    pygame.draw.rect(screen, (189, 195, 199), (430*resolution_scale, 720*resolution_scale, 250*resolution_scale, 55*resolution_scale))
    show_text("ENTER", 48, (0, 0, 0), (560, 750))

    #press escape to go back or something
    show_text("← ESC", 48, (255, 189, 144), (140, 920))


def draw_options_menu():
    screen.fill((144, 255, 189))

    show_text("OPTIONS", 72, (255, 189, 144), (640, 80))

    if option_selected == 0:
        difficulty_colour = (255, 189, 144)
    else:
        difficulty_colour = (0,0,0)
    show_text("Difficulty level", 32, difficulty_colour, (360, 200))
    show_text(difficulty_stages[difficulty_val], 32, difficulty_colour, (960, 200))

    if option_selected == 1:
        music_colour = (255, 189, 144)
    else:
        music_colour = (0,0,0)
    show_text("Music", 32, music_colour, (360, 300))
    show_text(music_stages[music_val], 32, music_colour, (960, 300))

    if option_selected == 2:
        sfx_colour = (255, 189, 144)
    else:
        sfx_colour = (0,0,0)
    show_text("SFX", 32, sfx_colour, (360, 400))
    show_text(sfx_stages[sfx_val], 32, sfx_colour, (960, 400))

    if option_selected == 3:
        timer_colour = (255, 189, 144)
    else:
        timer_colour = (0,0,0)
    show_text("show timer", 32, timer_colour, (360, 500))
    show_text(timer_stages[timer_val], 32, timer_colour, (960, 500))

    if option_selected == 4:
        screen_size_colour = (255, 189, 144)
    else:
        screen_size_colour = (0,0,0)
    show_text("Screen size", 32, screen_size_colour, (360, 600))
    show_text(screen_size_stages[screen_size_val], 32, screen_size_colour, (960, 600))

    pygame.draw.circle(screen, (255, 189, 144), (80*resolution_scale, (200 + 100 * option_selected)*resolution_scale), 16*resolution_scale)
    pygame.draw.polygon(screen, (255, 189, 144),
                        [[50*resolution_scale, (200 + 100 * option_selected)*resolution_scale], [20*resolution_scale, (230 + 100 * option_selected)*resolution_scale],
                         [20*resolution_scale, (170 + 100 * option_selected)*resolution_scale]])


def check_croc_collision():
    if max(player_x,past_coord[0][0]) - min(player_x+64, past_coord[0][0]+64) + 1 < 0 and max(player_y,past_coord[0][1]) - min(player_y+96, past_coord[0][1]+96) + 1 < 0:
        restart()
        generate_fail_comment(croc_fail_comments)
    else:
        pass


pygame.mixer.init(44100, -16, 2, 512)

if music_val == 0:
    chanel.play(ost,-1)

refresh_settings()
while running:

    if game_state == "start":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if start_option_selected > 0:
                        start_option_selected -= 1
                    else:
                        start_option_selected = 3
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if start_option_selected < 3:
                        start_option_selected += 1
                    else:
                        start_option_selected = 0
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if title_y == 128:
                        if start_option_selected == 0:
                            world_map = levels[0]
                            level_reset()
                        elif start_option_selected == 1:
                            game_state = "controls_menu"
                            screen_to_return_to = "start"
                        elif start_option_selected == 2:
                            game_state = "options_menu"
                            screen_to_return_to = "start"
                        else:
                            running = False

        draw_start_menu()

    elif game_state == "controls_menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = screen_to_return_to

        draw_controls_menu()

    elif game_state == "options_menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if option_selected > 0:
                        option_selected -= 1
                    else:
                        option_selected = 4
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if option_selected < 4:
                        option_selected += 1
                    else:
                        option_selected = 0
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT:
                    if option_selected == 0:
                        if difficulty_val < 2:
                            difficulty_val += 1
                        else:
                            difficulty_val = 0
                    elif option_selected == 1:
                        if music_val == 0:
                            chanel.play(blank_sound)
                            music_val = 1
                        else:
                            chanel.play(ost,-1)
                            music_val = 0
                    elif option_selected == 2:
                        if sfx_val == 0:
                            sfx_val = 1
                        else:
                            sfx_val = 0
                    elif option_selected == 3:
                        if timer_val == 0:
                            timer_val = 1
                        else:
                            timer_val = 0
                    elif option_selected == 4:
                        if screen_size_val < 2:
                            screen_size_val += 1
                        else:
                            screen_size_val = 0

                if event.key == pygame.K_LEFT:
                    if option_selected == 0:
                        if difficulty_val > 0:
                            difficulty_val -= 1
                        else:
                            difficulty_val = 2
                    elif option_selected == 1:
                        if music_val == 0:
                            music_val = 1
                            chanel.play(blank_sound)
                        else:
                            music_val = 0
                            chanel.play(ost, -1)
                    elif option_selected == 2:
                        if sfx_val == 0:
                            sfx_val = 1
                        else:
                            sfx_val = 0
                    elif option_selected == 3:
                        if timer_val == 0:
                            timer_val = 1
                        else:
                            timer_val = 0
                    elif option_selected == 4:
                        if screen_size_val > 0:
                            screen_size_val -= 1
                        else:
                            screen_size_val = 2

                if event.key == pygame.K_ESCAPE:
                    game_state = screen_to_return_to
                    refresh_settings()
        draw_options_menu()

    elif game_state == "level":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not start_moving:
                    start_moving = True
                    start_time[levels.index(world_map)] = pygame.time.get_ticks()

                # escape key
                if event.key == pygame.K_ESCAPE:
                    pause_start_time = pygame.time.get_ticks()
                    game_state = "pause"
                # space bar
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                    if state != "jump_up" and state != "fall":
                        state = "jump_up"
                        start_jump = player_y
                        y_velocity = max_y_up_velocity
                if event.key == pygame.K_RETURN:
                    restart()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and key[pygame.K_RIGHT] or key[pygame.K_a] and key[pygame.K_d]:
            x_velocity = 0
            if state != "fall" and state != "jump_up":
                state = "idle"

        elif key[pygame.K_LEFT] or key[pygame.K_a]:
            direction = "l"
            if (world_map[int((player_y + 1) // 64)][int(player_x // 64)] >= 1 or world_map[int((player_y + 95) // 64)][
                int(player_x // 64)] >= 1 or
                    world_map[int((player_y + 48) // 64)][int(player_x // 64)] >= 1):
                x_velocity = 0
            else:
                if x_velocity > -max_x_velocity:
                    x_velocity -= x_acceleration

            if state != "fall" and state != "jump_up":
                state = "run"

        elif key[pygame.K_RIGHT] or key[pygame.K_d]:
            direction = "r"
            if world_map[int((player_y + 1) // 64)][int(player_x // 64 + 1)] >= 1 or \
                    world_map[int((player_y + 95) // 64)][int(player_x // 64 + 1)] >= 1 or \
                    world_map[int((player_y + 48) // 64)][int(player_x // 64 + 1)] >= 1:
                x_velocity = 0
            else:
                if x_velocity < max_x_velocity:
                    x_velocity += x_acceleration
            if state != "fall" and state != "jump_up":
                state = "run"

        else:

            if x_velocity != 0:
                if x_velocity > 0:
                    x_velocity -= x_acceleration
                elif x_velocity < 0:
                    x_velocity += x_acceleration

                if -0.025 < x_velocity < 0.025:
                    x_velocity = 0
            if state != "fall" and state != "jump_up" and x_velocity <= 0:
                state = "idle"

        if state == "idle" or state == "run":
            y_velocity = 0

            player_y = (player_y // 64) * 64 + 32

            # checks if there is anything bellow player to check if you should fall and allows for cyote time
            if world_map[int((player_y + 97) // 64)][int((player_x + 1) // 64)] <= 0 and \
                    world_map[int((player_y + 97) // 64)][int((player_x + 63) // 64)] <= 0:
                if coyote == 0:
                    state = "fall"
                else:
                    coyote -= 1
            else:
                coyote = coyote_time

        elif state == "jump_up":
            if -0.025 < y_velocity < 0.025:
                state = "fall"
            else:
                y_velocity -= jumpspeed
        elif state == "fall":
            # feet collision and gravity
            if world_map[int((player_y + 96) // 64)][int((player_x + 1) // 64)] >= 1 or \
                    world_map[int((player_y + 96) // 64)][int((player_x + 63) // 64)] >= 1:

                state = "idle"
            else:
                if y_velocity < max_y_down_velocity:
                    y_velocity -= gravity_fall

        player_y = round(player_y, 2)
        player_x = round(player_x, 2)

        # print(player_x, "                ", player_y)
        # print(state)
        # print(x_velocity)

        # spike fail
        if y_velocity < 0:
            if world_map[int((player_y + 95 + y_velocity) // 64)][int((player_x + 1) // 64)] == -1 or \
                    world_map[int((player_y + 95 + y_velocity) // 64)][int((player_x + 63) // 64)] == -1:
                x_velocity = 0
                y_velocity = 0
                generate_fail_comment(spike_fail_comments)
                restart()
        else:
            if world_map[int((player_y + 95) // 64)][int((player_x + 1) // 64)] == -1 or \
                    world_map[int((player_y + 95) // 64)][int((player_x + 63) // 64)] == -1:
                x_velocity = 0
                y_velocity = 0
                generate_fail_comment(spike_fail_comments)
                restart()

        if not start_moving and state != "idle":
            start_moving = True
            start_time[levels.index(world_map)] = pygame.time.get_ticks()

        if len(past_coord) == croc_time:
            check_croc_collision()

        #spring
        if world_map[int((player_y + 97) // 64)][int((player_x + 1) // 64)] == 99 or \
                world_map[int((player_y + 97) // 64)][int((player_x + 63) // 64)] == 99:
            state = "jump_up"
            y_velocity = (max_y_up_velocity * 1.5)

        # flag
        if world_map[int(player_y // 64)][int(player_x // 64)] == -99 or world_map[int((player_y + 96) // 64)][
            int(player_x // 64)] == -99 or world_map[int(player_y // 64)][int((player_x + 65) // 64)] == -99 or \
                world_map[int((player_y + 96) // 64)][int((player_x + 65) // 64)] == -99 or \
                world_map[int((player_y + 48) // 64)][int((player_x - 1) // 64)] == -99 or \
                world_map[int((player_y + 48) // 64)][int((player_x + 65) // 64)] == -99:
            time[levels.index(world_map)] -= buffer_time
            if world_map == levels[-1]:
                game_state = "end"
                end_time[levels.index(world_map)] = pygame.time.get_ticks()
                for i in range(len(end_time)):
                    time[i] = (end_time[i]-start_time[i])/1000
                pygame.time.set_timer(pygame.USEREVENT, 500)
            else:
                end_time[levels.index(world_map)] = pygame.time.get_ticks()
                if world_map == levels[0]:
                    world_map = levels[1]
                    level_reset()
                elif world_map == levels[1]:
                    world_map = levels[2]
                    level_reset()

        if x_velocity > 0:
            x = player_x + x_velocity + 64
            if (world_map[int((player_y + 1) // 64)][int(x // 64)] <= 0 and world_map[int((player_y + 95) // 64)][
                int(x // 64)] <= 0 and
                    world_map[int((player_y + 48) // 64)][int(x // 64)] <= 0):
                if state == "jump_up" or state == "fall":
                    player_x += x_velocity
                else:
                    player_x += x_velocity
            else:
                # player_x = player_x//64 * 64
                x_velocity = 0
        elif x_velocity < 0:
            x = player_x + x_velocity
            if (world_map[int((player_y + 1) // 64)][int(x // 64)] <= 0 and world_map[int((player_y + 95) // 64)][
                int(x // 64)] <= 0 and
                    world_map[int((player_y + 48) // 64)][int(x // 64)] <= 0):
                if state == "jump_up" or state == "fall":
                    player_x += x_velocity
                else:
                    player_x += x_velocity
            else:
                x_velocity = 0

        if y_velocity > 0:
            y = player_y - y_velocity
            if world_map[int(y // 64)][int((player_x + 1) // 64)] <= 0 and world_map[int(y // 64)][int((player_x + 63) // 64)] <= 0:
                player_y -= y_velocity
            else:
                y_velocity = 0
                state = "fall"
        elif y_velocity < 0:
            y = player_y + 96 - y_velocity
            if world_map[int(y // 64)][int((player_x + 1) // 64)] <= 0 and world_map[int(y // 64)][int((player_x + 63) // 64)] <= 0:
                player_y -= y_velocity
            else:
                y_velocity = 0
                state = "idle"

        if start_moving:
            past_coord.append((player_x,player_y,direction))

        draw_level(world_map)

    elif game_state == "pause":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # escape key
                if event.key == pygame.K_ESCAPE:
                    game_state = "level"
                    buffer_time += pygame.time.get_ticks() - pause_start_time
                if event.key == pygame.K_UP:
                    if pause_option == 0:
                        pause_option = 3
                    else:
                        pause_option -= 1
                if event.key == pygame.K_DOWN:
                    if pause_option == 3:
                        pause_option = 0
                    else:
                        pause_option += 1
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if pause_option == 0:
                        game_state = "level"
                    elif pause_option == 1:
                        game_state = "controls_menu"
                        screen_to_return_to = "pause"
                    elif pause_option == 2:
                        game_state = "options_menu"
                        screen_to_return_to = "pause"
                    elif pause_option == 3:
                        game_state = "start"
            draw_pause_menu()

    elif game_state == "end":
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                end_count += 1
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if end_count > 3:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if end_option == 0:
                            world_map = levels[0]
                            level_reset()
                        elif end_option == 1:
                            game_state = "start"
                    if event.key == pygame.K_UP:
                        if end_option == 0:
                            end_option = 1
                        else:
                            end_option = 0
                    if event.key == pygame.K_DOWN:
                        if end_option == 0:
                            end_option = 1
                        else:
                            end_option = 0

            draw_end_screen()

    clock.tick(FPS)
    #print(pygame.time.Clock.get_fps(clock))

    pygame.display.flip()

pygame.quit()
sys.exit()