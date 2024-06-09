import pygame
import sys
import csv

clock = pygame.time.Clock()
#set game FPS
FPS = 60


pygame.init()
BGC = (255, 255, 255)
screen = pygame.display.set_mode((1280, 960))

world_map = []

with open("map.csv", newline="") as csvfile:
    mapreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in mapreader:
        world_map.append(row[0].split(","))
print((world_map[0]))

for i in range(len(world_map)):
    for o in range(len(world_map[i])):
        if world_map[i][o] != "x":
            world_map[i][o] = int(world_map[i][o])


running = True

player_x = 960
player_y = 320
direction = "r"

state = "idle"


img = pygame.image.load("assets\\idle1_right.png").convert_alpha()
background_img = pygame.image.load("assets\\background.png").convert()

x_velocity = 0
y_velocity = 0

max_x_velocity = 10
max_y_up_velocity = 7
max_y_down_velocity = 10

jumpspeed = 0.1
gravity_fall = 0.5
x_acceleration = 0.25
start_jump = 0


# sprite stages
idle_sprite = 1
left_sprite = 1
right_sprite = 1


#length of cyote(frames)
coyote_time = 5
##update cyote
coyote = coyote_time


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


def load_sprites():
    global grass_img, dirt_img,leftcup_img,rightcup_img,bottomcup_img,topcup_img,bottomleftcorner_img,bottomrightcorner_img,topleftcorner_img,toprightcorner_img,right_img,\
    left_img, top_img,bottom_img,horizontaltube_img,verticaltube_img
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


load_sprites()


def draw_screen():
    global player

    get_sprite()
    #screen.fill(BGC)
    screen.blit(background_img, (0,0))

    player_offset = player_x % 64 + 32
    player_bit = (player_x//64)-9.5

    tile_img = pygame.image.load("assets\\grass.png").convert()

    #tile map
    for y in range(15):
        for x in range(22):
            tile = world_map[y][int(player_bit + x)]
            # grass
            if tile == 1:
                screen.blit(grass_img, (x * 64 - player_offset, y * 64))
            # dirt
            elif tile == 2:
                screen.blit(dirt_img, (x * 64 - player_offset, y * 64))
            #right side missing/left cup
            elif tile == 3:
                screen.blit(leftcup_img, (x * 64 - player_offset, y * 64))
            #left side missing/right cup
            elif tile == 4:
                screen.blit(rightcup_img, (x * 64 - player_offset, y * 64))
            # top side missing/bottom cup
            elif tile == 5:
                screen.blit(bottomcup_img, (x * 64 - player_offset, y * 64))
            # bottom side missing/top cup
            elif tile == 6:
                screen.blit(topcup_img, (x * 64 - player_offset, y * 64))
            #bottom left corner
            elif tile == 7:
                screen.blit(bottomleftcorner_img, (x * 64 - player_offset, y * 64))
            #bottom right corner
            elif tile == 8:
                screen.blit(bottomrightcorner_img, (x * 64 - player_offset, y * 64))
            #top left corner
            elif tile == 9:
                screen.blit(topleftcorner_img, (x * 64 - player_offset, y * 64))
            #top right corner
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
            #bottom
            elif tile == 14:
                screen.blit(bottom_img, (x * 64 - player_offset, y * 64))
            # horizontal tube
            elif tile == 15:
                screen.blit(horizontaltube_img, (x * 64 - player_offset, y * 64))
            # vertical tube
            elif tile == 16:
                screen.blit(verticaltube_img, (x * 64 - player_offset, y * 64))

    screen.blit(img, (608, player_y))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # escape key
            if event.dict["key"] == 27:
                running = False
            # space bar
            if event.dict["key"] == 32:
                if state != "jump_up" and state != "fall":
                    state = "jump_up"
                    start_jump = player_y
                    y_velocity = max_y_up_velocity

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and key[pygame.K_RIGHT]:
        if state != "fall" and state != "jump_up":
            state = "idle"
            x_velocity = 0

    elif key[pygame.K_LEFT]:
        direction = "l"
        if (world_map[int((player_y + 1) // 64)][int(player_x // 64)] >= 1 or world_map[int((player_y + 95) // 64)][int(player_x // 64)] >= 1 or
                world_map[int((player_y + 48) // 64)][int(player_x // 64)] >= 1):
            x_velocity = 0
        else:
            if x_velocity > -max_x_velocity:
                x_velocity -= x_acceleration

        if state != "fall" and state != "jump_up":
            state = "run"

    elif key[pygame.K_RIGHT]:
        direction = "r"
        if (world_map[int((player_y + 1) // 64)][int(player_x // 64 + 1)] >= 1 or world_map[int((player_y + 95) // 64)][int(player_x // 64 + 1)] >= 1 or world_map[int((player_y + 48) // 64)][int(player_x // 64 + 1)] >= 1):
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
        if state != "fall" and state != "jump_up" and x_velocity == 0:
            state = "idle"

    if state == "idle" or state == "run":
        y_velocity = 0

        player_y = (player_y // 64) * 64 + 32

        # checks if there is anything bellow player to check if you should fall and allows for cyote time
        if world_map[int((player_y + 97) // 64)][int(player_x // 64)] == 0 and world_map[int((player_y + 97) // 64)][int(player_x // 64 + 1)] == 0:
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
        if world_map[int((player_y + 96) // 64)][int((player_x + 1) // 64)] >= 1 or world_map[int((player_y + 96) // 64)][int((player_x + 63) // 64)] >= 1:
            print(1)

            state = "idle"
        else:
            if y_velocity < max_y_down_velocity:
                y_velocity -= gravity_fall

    #collisions()

    player_y = round(player_y, 2)
    player_x = round(player_x, 2)

    #print(player_x, "                ", player_y)
    #print(state)
    print(x_velocity)

    clock.tick(FPS)
    #print(pygame.time.Clock.get_fps(clock))

    if x_velocity > 0:
        x = player_x + x_velocity + 64
        if (world_map[int((player_y + 1) // 64)][int(x // 64)] == 0 and world_map[int((player_y + 95) // 64)][int(x // 64)] == 0 and
        world_map[int((player_y + 48) // 64)][int(x // 64)] == 0):
            if state == "jump_up" or state == "fall":
                player_x += x_velocity / 1.5
            else:
                player_x += x_velocity
        else:
            #player_x = player_x//64 * 64
            x_velocity = 0
    elif x_velocity < 0:
        x = player_x + x_velocity
        if (world_map[int((player_y + 1) // 64)][int(x // 64)] == 0 and world_map[int((player_y + 95) // 64)][int(x // 64)] == 0 and
        world_map[int((player_y + 48) // 64)][int(x // 64)] == 0):
            if state == "jump_up" or state == "fall":
                player_x += x_velocity / 1.5
            else:
                player_x += x_velocity
        else:
            x_velocity = 0

    if y_velocity > 0:
        y = player_y - y_velocity
        if world_map[int(y // 64)][int((player_x + 1) // 64)] == 0 or world_map[int(y // 64)][int((player_x + 63) // 64)] == 0:
            player_y -= y_velocity
        else:
            y_velocity = 0
            state = "fall"
    elif y_velocity < 0:
        y = player_y + 96 - y_velocity
        if world_map[int(y // 64)][int((player_x + 1) // 64)] == 0 or world_map[int(y // 64)][int((player_x + 63) // 64)] == 0:
            player_y -= y_velocity
        else:
            y_velocity = 0
            state = "idle"

    draw_screen()
    pygame.display.flip()

pygame.quit()
sys.exit()
