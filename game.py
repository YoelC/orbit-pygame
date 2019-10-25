import pygame
import config
from classes.cube import Cube
from math import atan2, degrees, radians, sin, cos

pygame.init()
pygame.font.init()

win = pygame.display.set_mode((config.window_width, config.window_height))
pygame.display.set_caption('Physics')

tick = 0
run = True
clicking_orbit = False
clicking_player = False

player = Cube(
    pos=(
        (config.window_width/2) - config.player_width/2,
        (config.window_height/2) - config.player_height/2,
        config.player_width,
        config.player_height
    ),
    color=(255, 255, 255))

center_orbit = Cube(
    pos=(
        (config.window_width/2) - config.orbit_width/2,
        (config.window_height/2) - config.orbit_height/2,
        config.orbit_width,
        config.orbit_height
    ),
    color=(255, 0, 0))


pos_x, pos_y = center_orbit.x, center_orbit.y
while run:
    try:
        pygame.time.delay(int(1000/config.fps))
    except ZeroDivisionError:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)

    keys = {
        'left': pygame.key.get_pressed()[pygame.K_LEFT],
        'right': pygame.key.get_pressed()[pygame.K_RIGHT],
        'up': pygame.key.get_pressed()[pygame.K_UP],
        'down': pygame.key.get_pressed()[pygame.K_DOWN],
        'space': pygame.key.get_pressed()[pygame.K_SPACE],
        'esc': pygame.key.get_pressed()[pygame.K_ESCAPE],
        'left click': pygame.mouse.get_pressed()[0],
        'r': pygame.key.get_pressed()[pygame.K_r]
    }

    if keys['left']:
        player.x_vel -= 2.5

    if keys['right']:
        player.x_vel += 2.5

    if keys['up']:
        player.y_vel -= 2.5

    if keys['down']:
        player.y_vel += 2.5

    if keys['left click']:
        if mouse_rect.colliderect(center_orbit.get_rect()) or clicking_orbit:
            clicking_orbit = True
            pos_x, pos_y = pygame.mouse.get_pos()
            center_orbit.x = pygame.mouse.get_pos()[0] - center_orbit.width/2
            center_orbit.y = pygame.mouse.get_pos()[1] - center_orbit.height/2

        if mouse_rect.colliderect(player.get_rect()) or clicking_player:
            clicking_player = True
            player.x = pygame.mouse.get_pos()[0] - player.width/2
            player.y = pygame.mouse.get_pos()[1] - player.height/2

            try:
                delta_x = player.x - previous_pos_x
                delta_y = player.y - previous_pos_y
            except NameError:
                delta_x = 0
                delta_y = 0
                pass

            previous_pos_x = player.x
            previous_pos_y = player.y

            player.x_vel = 0
            player.y_vel = 0

    else:
        if clicking_orbit:
            clicking_orbit = False

        if clicking_player:
            clicking_player = False
            player.x_vel = delta_x
            player.y_vel = delta_y
            delta_x = 0
            delta_y = 0

    if keys['r']:
        player.x = (config.window_width/2) - player.width/2
        player.y = (config.window_height/2) - player.height/2

        player.x_vel = 0
        player.y_vel = 0

    angle_to_pos = ((degrees(atan2(pos_x - player.get_center()[0], pos_y - player.get_center()[1]))) + 270) % 360

    player.x_vel += cos(radians(angle_to_pos))
    player.y_vel -= sin(radians(angle_to_pos))

    if keys['space']:
        player.x_vel = 0
        player.y_vel = 0

    player.calculate_distance()

    temp_rect = win.get_rect()
    temp_rect.width -= player.width*2
    temp_rect.height -= player.height*2
    temp_rect.x += player.width
    temp_rect.y += player.height

    if not player.get_rect().colliderect(temp_rect):
        print('ERROR: Outside world border')

    win.fill(0)
    player.draw(win)
    center_orbit.draw(win)
    pygame.display.flip()

    tick += 1
