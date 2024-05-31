import pygame
import sys

pygame.init()
BGC = (255, 255, 255)
screen = pygame.display.set_mode((1280, 960))

map = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, "x"],
       [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "x"],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "x"]]

running = True
gravity = 2
player_x = 64
player_y = 640

speed = 2
jumpspeed = 2

state = "idle"

start_jump = 0

img = pygame.image.load("assets\idle_test.png")

#sprite stages
idle_sprite = 1
left_sprite = 1
right_sprite = 1

def get_sprite():
    global img, idle, left_sprite, right_sprite

    if state == "idle":
        if idle_sprite == 1:
            img = pygame.image.load("assets\idle_test.png")

    if state == "r_right":
        if 1 <= right_sprite <= 10:
            img = pygame.image.load("assets\\right1.png")
            right_sprite += 1
        elif 11 <= right_sprite <= 20:
            img = pygame.image.load("assets\\right2.png")
            right_sprite += 1
        elif 21 <= right_sprite <= 30:
            img = pygame.image.load("assets\\right3.png")
            right_sprite += 1
        elif 31 <= right_sprite <= 40:
            img = pygame.image.load("assets\\right4.png")
            right_sprite += 1
        else:
            right_sprite = 1

    if state == "r_left":
        if 1 <= left_sprite <= 10:
            img = pygame.image.load("assets\\left1.png")
            left_sprite += 1
        elif 11 <= left_sprite <= 20:
            img = pygame.image.load("assets\\left2.png")
            left_sprite += 1
        elif 21 <= left_sprite <= 30:
            img = pygame.image.load("assets\\left3.png")
            left_sprite += 1
        elif 31 <= left_sprite <= 40:
            img = pygame.image.load("assets\\left4.png")
            left_sprite += 1
        else:
            left_sprite = 1





def draw_screen():
    global player

    get_sprite()
    screen.fill(BGC)
    screen.blit(screen, player)
    #player = pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, 64, 96))
    screen.blit(img, (player_x,player_y))

    y_count = 0
    for y in map:
        x_count = 0
        for x in y:
            if x == 1:
                pygame.draw.rect(screen, (0, 0, 0), (x_count * 64, y_count * 64, 64, 64))
            x_count += 1
        y_count += 1


player = pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, 64, 96))

past_x = player_x
past_y = player_y

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

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and key[pygame.K_RIGHT]:
        if state != "fall" and state != "jump_up":
            state = "idle"
    elif key[pygame.K_LEFT]:
        if player_x > 0 and not (
                map[(player_y + 1) // 64][player_x // 64] == 1 or map[(player_y + 95) // 64][player_x // 64] == 1 or
                map[(player_y + 48) // 64][player_x // 64] == 1):
            player_x -= speed
        if state != "fall" and state != "jump_up":
            state = "r_left"
    elif key[pygame.K_RIGHT]:
        if player_x <= 1216 and not (map[(player_y + 1) // 64][player_x // 64 + 1] == 1 or map[(player_y + 95) // 64][player_x // 64 + 1] == 1 or map[(player_y + 48) // 64][player_x // 64 + 1] == 1):
            player_x += speed
        if state != "fall" and state != "jump_up":
            state = "r_right"
    else:
        if state != "fall" and state != "jump_up":
            state = "idle"

    # checks if there is anything bellow player to check if you should fall
    if state == "idle" or state == "r_left" or state == "r_right":
        if player_y > past_y:
            state = "fall"
        if map[(player_y + 97) // 64][player_x // 64] == 0 and map[(player_y + 97) // 64][player_x // 64 + 1] == 0:
            state = "fall"
    elif state == "jump_up":
        if player_y <= start_jump - 256:
            state = "fall"
        else:
            # set jump height
            player_y -= jumpspeed
    elif state == "fall":
        # bottom collision and gravity
        if map[(player_y + 96) // 64][(player_x + 1) // 64] == 1 or map[(player_y + 96) // 64][
            (player_x + 63) // 64] == 1:
            state = "idle"
        else:
            player_y += gravity

    # top
    if map[player_y // 64][(player_x + 1) // 64] == 1 or map[player_y // 64][(player_x + 63) // 64] == 1:
        state = "fall"
    # left

    past_x = player_x
    past_y = player_y

    print(state)

    draw_screen()
    pygame.display.flip()

pygame.quit()
sys.exit()
