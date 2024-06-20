import csv
import sys

import pygame
import spritesheet

clock = pygame.time.Clock()
# set game FPS
FPS = 60

end_count = 0

pygame.init()
BGC = (255, 255, 255)
screen = pygame.display.set_mode((1280, 960))


def file_load(file_name):
    file_scan = []
    with open(f"{file_name}.csv", newline="") as csvfile:
        mapreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in mapreader:
            file_scan.append(row[0].split(","))

    for i in range(len(file_scan)):
        for o in range(len(file_scan[i])):
            file_scan[i][o] = int(file_scan[i][o])

    return file_scan


levels = [file_load("level1"), file_load("level2")]

world_map = levels[0]

running = True

player_x = int(world_map[-1][0])
player_y = int(world_map[-1][1])
direction = "r"

state = "idle"
game_state = "start"

background_img = pygame.image.load("assets\\background.png").convert()

grass_img = pygame.image.load("assets\\grass.png").convert()
dirt_img = pygame.image.load("assets\\dirt.png").convert()
leftcup_img = pygame.image.load("assets\\grass_leftcup.png").convert()
rightcup_img = pygame.image.load("assets\\grass_rightcup.png").convert()
bottomcup_img = pygame.image.load("assets\\grass_bottomcup.png").convert()
topcup_img = pygame.image.load("assets\\grass_topcup.png").convert()
bottomleftcorner_img = pygame.image.load("assets\\grass_bottomleftcorner.png").convert()
bottomrightcorner_img = pygame.image.load("assets\\grass_bottomrightcorner.png").convert()
topleftcorner_img = pygame.image.load("assets\\grass_topleftcorner.png").convert()
toprightcorner_img = pygame.image.load("assets\\grass_toprightcorner.png").convert()
right_img = pygame.image.load("assets\\grass_right.png").convert()
left_img = pygame.image.load("assets\\grass_left.png").convert()
top_img = pygame.image.load("assets\\grass_top.png").convert()
bottom_img = pygame.image.load("assets\\grass_bottom.png").convert()
horizontaltube_img = pygame.image.load("assets\\grass_horizontal_tube.png").convert()
verticaltube_img = pygame.image.load("assets\\grass_vertical_tube.png").convert()
spike = pygame.image.load("assets\\spike.png").convert_alpha()
flag = pygame.image.load("assets\\flag.png").convert_alpha()
spring = pygame.image.load("assets\\spring.png").convert_alpha()

croc_spritesheet_l = spritesheet.SpriteSheet("assets\\crocs_spritesheet_l.png")
croc_spritesheet_l = croc_spritesheet_l.images_at(((0,0,64,96),(64,0,64,96),(128,0,64,96),(192,0,64,96),(256,0,64,96),(320,0,64,96),(384,0,64,96),(448,0,64,96),(512,0,64,96),(576,0,64,96),(640,0,64,96),(704,0,64,96),(768,0,64,96)), colorkey=(0,0,0))

croc_spritesheet_r = spritesheet.SpriteSheet("assets\\crocs_spritesheet_r.png")
croc_spritesheet_r = croc_spritesheet_r.images_at(((0,0,64,96),(64,0,64,96),(128,0,64,96),(192,0,64,96),(256,0,64,96),(320,0,64,96),(384,0,64,96),(448,0,64,96),(512,0,64,96),(576,0,64,96),(640,0,64,96),(704,0,64,96),(768,0,64,96)), colorkey=(0,0,0))

ost = pygame.mixer.Sound("assets\\Platformy OST.mp3")
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

# length of cyote(frames)
coyote_time = 5
##update cyote
coyote = coyote_time

#follower
start_moving = False
past_coord = []
croc_num = 0


def level_reset():
    global player_x, player_y, game_state, x_velocity, y_velocity, start_moving, past_coord

    start_moving = False
    past_coord = []

    player_x = int(world_map[-1][0])
    player_y = int(world_map[-1][1])

    x_velocity = 0
    y_velocity = 0

    game_state = "level"


def restart():
    level_reset()

    pygame.mixer.Sound.play(fail, 0)


def get_sprite():
    global img, left_sprite, right_sprite, idle_sprite

    if state == "idle" and direction == "r":
        if 1 <= idle_sprite <= 100:
            img = pygame.image.load("assets\\idle1_right.png").convert_alpha()
            idle_sprite += 1
        elif 101 <= idle_sprite <= 200:
            img = pygame.image.load("assets\\idle2_right.png").convert_alpha()
            idle_sprite += 1
        else:
            idle_sprite = 1

    if state == "idle" and direction == "l":
        if 1 <= idle_sprite <= 100:
            img = pygame.image.load("assets\\idle1_left.png").convert_alpha()
            idle_sprite += 1
        elif 101 <= idle_sprite <= 200:
            img = pygame.image.load("assets\\idle2_left.png").convert_alpha()
            idle_sprite += 1
        else:
            idle_sprite = 1

    if state == "run" and direction == "r":
        if 1 <= right_sprite <= 10:
            img = pygame.image.load("assets\\right1.png").convert_alpha()
            right_sprite += 1
        elif 11 <= right_sprite <= 20:
            img = pygame.image.load("assets\\right2.png").convert_alpha()
            right_sprite += 1
        elif 21 <= right_sprite <= 30:
            img = pygame.image.load("assets\\right3.png").convert_alpha()
            right_sprite += 1
        elif 31 <= right_sprite <= 40:
            img = pygame.image.load("assets\\right4.png").convert_alpha()
            right_sprite += 1
        else:
            right_sprite = 1

    if state == "run" and direction == "l":
        if 1 <= left_sprite <= 10:
            img = pygame.image.load("assets\\left1.png").convert_alpha()
            left_sprite += 1
        elif 11 <= left_sprite <= 20:
            img = pygame.image.load("assets\\left2.png").convert_alpha()
            left_sprite += 1
        elif 21 <= left_sprite <= 30:
            img = pygame.image.load("assets\\left3.png").convert_alpha()
            left_sprite += 1
        elif 31 <= left_sprite <= 40:
            img = pygame.image.load("assets\\left4.png").convert_alpha()
            left_sprite += 1
        else:
            left_sprite = 1

    if state == "jump_up":
        if direction == "l":
            img = pygame.image.load("assets\\jump_l.png").convert_alpha()
        else:
            img = pygame.image.load("assets\\jump_r.png").convert_alpha()

    if state == "fall":
        if direction == "l":
            img = pygame.image.load("assets\\fall_l.png").convert_alpha()
        else:
            img = pygame.image.load("assets\\fall_r.png").convert_alpha()


def draw_level(world_map):
    global player,past_coord, croc_num

    get_sprite()
    # screen.fill(BGC)
    screen.blit(background_img, (0, 0))

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
                screen.blit(spike, (x * 64 - player_offset, y * 64))
            # grass
            if tile == 1:
                screen.blit(grass_img, (x * 64 - player_offset, y * 64))
            # dirt
            elif tile == 2:
                screen.blit(dirt_img, (x * 64 - player_offset, y * 64))
            # right side missing/left cup
            elif tile == 3:
                screen.blit(leftcup_img, (x * 64 - player_offset, y * 64))
            # left side missing/right cup
            elif tile == 4:
                screen.blit(rightcup_img, (x * 64 - player_offset, y * 64))
            # top side missing/bottom cup
            elif tile == 5:
                screen.blit(bottomcup_img, (x * 64 - player_offset, y * 64))
            # bottom side missing/top cup
            elif tile == 6:
                screen.blit(topcup_img, (x * 64 - player_offset, y * 64))
            # bottom left corner
            elif tile == 7:
                screen.blit(bottomleftcorner_img, (x * 64 - player_offset, y * 64))
            # bottom right corner
            elif tile == 8:
                screen.blit(bottomrightcorner_img, (x * 64 - player_offset, y * 64))
            # top left corner
            elif tile == 9:
                screen.blit(topleftcorner_img, (x * 64 - player_offset, y * 64))
            # top right corner
            elif tile == 10:
                screen.blit(toprightcorner_img, (x * 64 - player_offset, y * 64))
            # right
            elif tile == 11:
                screen.blit(right_img, (x * 64 - player_offset, y * 64))
            # left
            elif tile == 12:
                screen.blit(left_img, (x * 64 - player_offset, y * 64))
            # top
            elif tile == 13:
                screen.blit(top_img, (x * 64 - player_offset, y * 64))
            # bottom
            elif tile == 14:
                screen.blit(bottom_img, (x * 64 - player_offset, y * 64))
            # horizontal tube
            elif tile == 15:
                screen.blit(horizontaltube_img, (x * 64 - player_offset, y * 64))
            # vertical tube
            elif tile == 16:
                screen.blit(verticaltube_img, (x * 64 - player_offset, y * 64))
            #spring
            elif tile == 99:
                screen.blit(spring, (x * 64 - player_offset, y * 64))

            #flag
            elif tile == -99:
                screen.blit(flag, (x * 64 - player_offset, y * 64))

    if player_x < 608:
        screen.blit(img, (player_x, player_y))
    elif player_x > len(world_map[0]) * 64 - 736:
        screen.blit(img, ((1346 - (len(world_map[0]) * 64 - player_x)), player_y))
    else:
        screen.blit(img, (608, player_y))

    if len(past_coord) > 60:
        croc_num += 1

        if past_coord[0][2] == "r":
            croc = croc_spritesheet_r[croc_num//6]
        else:
            croc = croc_spritesheet_l[croc_num // 6]
        if croc_num == 66:
            croc_num = 0

        if player_x < 608:
            screen.blit(croc, (past_coord[0][0],past_coord[0][1]))
        elif player_x > len(world_map[0]) * 64 - 736:
            screen.blit(croc, (1346 - (len(world_map[0]) * 64 - past_coord[0][0]), past_coord[0][1]))
        else:
            screen.blit(croc, (608-(player_x-past_coord[0][0]),past_coord[0][1]))

        past_coord.pop(0)


def draw_start_menu():
    global title_y

    screen.fill((144, 255, 189))

    title = pygame.font.Font("PressStart2P.ttf", 96).render("Platformy", True, (0, 0, 0))
    title_rect = title.get_rect()
    title_rect.center = (640, title_y)

    start_prompt_text = pygame.font.Font("PressStart2P.ttf", 48).render("Press any key to start", True, (0, 0, 0))
    start_prompt_text_rect = start_prompt_text.get_rect()
    start_prompt_text_rect.center = (640, 520)

    if title_y != 256:
        title_y += 2

    if title_y == 256:
        screen.blit(start_prompt_text, start_prompt_text_rect)

    screen.blit(title, title_rect)


def draw_end_screen():
    screen.fill((255, 181, 68))

    victory = pygame.font.Font("PressStart2P.ttf", 96).render("Victory", True, (68, 142, 255))
    victory_rect = victory.get_rect()
    victory_rect.center = (640, 256)

    restart_prompt = pygame.font.Font("PressStart2P.ttf", 32).render("Press any key to have another go", True,
                                                                     (68, 142, 255))
    restart_prompt_rect = restart_prompt.get_rect()
    restart_prompt_rect.center = (640, 640)

    screen.blit(victory, victory_rect)

    if end_count > 3:
        screen.blit(restart_prompt, restart_prompt_rect)


def draw_pause_menu():
    pygame.draw.rect(screen, (0, 0, 0), (320, 0, 640, 1280))

    Pause_text = pygame.font.Font("PressStart2P.ttf", 96).render("Pause", True, (255, 255, 255))
    Pause_text_rect = Pause_text.get_rect()
    Pause_text_rect.center = (640, 256)

    screen.blit(Pause_text, Pause_text_rect)


def check_croc_collision():
    if max(player_x,past_coord[0][0]) - min(player_x+64, past_coord[0][0]+64) + 1 < 0 and max(player_y,past_coord[0][1]) - min(player_y+96, past_coord[0][1]+96) + 1 < 0:
        restart()
    else:
        pass


pygame.mixer.Sound.play(ost, 1000)

while running:
    if game_state == "start":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                level_reset()
        draw_start_menu()

    elif game_state == "level":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not start_moving:
                    start_moving = True

                # escape key
                if event.key == pygame.K_ESCAPE:
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

        # fail
        if y_velocity < 0:
            if world_map[int((player_y + 95 + y_velocity) // 64)][int((player_x + 1) // 64)] == -1 or \
                    world_map[int((player_y + 95 + y_velocity) // 64)][int((player_x + 63) // 64)] == -1:
                x_velocity = 0
                y_velocity = 0
                restart()
        else:
            if world_map[int((player_y + 95) // 64)][int((player_x + 1) // 64)] == -1 or \
                    world_map[int((player_y + 95) // 64)][int((player_x + 63) // 64)] == -1:
                x_velocity = 0
                y_velocity = 0
                restart()

        if not start_moving and state != "idle":
            start_moving = True

        if len(past_coord) == 60:
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
            if world_map == levels[-1]:
                game_state = "end"
                pygame.time.set_timer(pygame.USEREVENT, 500)
            else:
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
            if world_map[int(y // 64)][int((player_x + 1) // 64)] <= 0 or world_map[int(y // 64)][int((player_x + 63) // 64)] <= 0:
                player_y -= y_velocity
            else:
                y_velocity = 0
                state = "fall"
        elif y_velocity < 0:
            y = player_y + 96 - y_velocity
            if world_map[int(y // 64)][int((player_x + 1) // 64)] <= 0 or world_map[int(y // 64)][int((player_x + 63) // 64)] <= 0:
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
            draw_pause_menu()

    elif game_state == "end":
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                end_count += 1
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if end_count > 3:
                    world_map = levels[0]
                    level_reset()

            draw_end_screen()

    clock.tick(FPS)
    # print(pygame.time.Clock.get_fps(clock))

    pygame.display.flip()

pygame.quit()
sys.exit()
