import concurrent.futures
from designer import *
from dataclasses import dataclass
from random import randint
import pygame
import time
import threading
from queue import Queue

#on platform variable
on_platform = False

#Determines player character speed
WORKER_SPEED = 10

#Determines player character jump height
WORKER_HEIGHT = 0

#Jumping Variable
jumping = False

#Determines how fast platforms fall
PLATFORM_SPEED = 3

#Sets starting time for game
game_time = 0

#Determines how fast obstacles fall
Obstacles_fall_speed = 5

@dataclass
class World:
    game_over: DesignerObject
    gaming_timer: DesignerObject
    player_character: DesignerObject
    obstacles: list[DesignerObject]
    platforms: list[DesignerObject]

def create_world() -> World:
    """ Creates the game world """
    return World(text("black", "", 30),
                 text("black", "0:00", 20, 25, 20),
                 create_player(), [], [])

def create_platforms() -> DesignerObject:
    """ Creates platforms for the player """
    rand_x_coord = randint(0, 600)
    platform = line("black", rand_x_coord, -5, rand_x_coord + 300, -5, 3)
    return platform

def make_platforms(world: World):
    if len(world.platforms) < 5:# and game_time % 10 == 0:
        world.platforms.append(create_platforms())

def drop_platforms(world: World):
    for platform in world.platforms:
        platform.y += PLATFORM_SPEED

def destroy_platforms(world: World):
    kept = []
    for platform in world.platforms:
        if platform.y < get_height():
            kept.append(platform)
        else:
            destroy(platform)
    world.platforms = kept

def player_on_platform(world: World):
    global on_platform
    if on_platform:
        world.player_character.y = world.platforms[0].y - 15
        if world.player_character.y > get_height() - 20:
            on_platform = False
        if world.player_character.x < world.platforms[0].x or world.player_character.x > world.platforms[0].x + 300:
            on_platform = False
            world.player_character.y += 10

def create_obstacles() -> DesignerObject:
    """ Creates obstacles for the player """
    obstacle = emoji("🔻")
    obstacle.scale_x = 1.5
    obstacle.scale_y = 1.5
    obstacle.x = randint(0,get_width())
    obstacle.y = 0
    return obstacle

def make_obstacles(world: World):
    cap_obstacles = len(world.obstacles) < 11
    random_chance = randint(1, 75) == 50
    if cap_obstacles and random_chance:
        world.obstacles.append(create_obstacles())

def drop_obstacles(world: World):
    for obstacle in world.obstacles:
        obstacle.y += Obstacles_fall_speed

def destroy_obstacles(world: World):
    kept = []
    for obstacle in world.obstacles:
        if obstacle.y < get_height():
            kept.append(obstacle)
        else:
            destroy(obstacle)
    world.obstacles = kept

def collide_with_obstacle(world: World) -> bool:
    for obstacle in world.obstacles:
        if world.player_character.x >= obstacle.x - 25 and world.player_character.x <= obstacle.x + 25:
            if world.player_character.y >= obstacle.y - 25 and world.player_character.y <= obstacle.y + 25:
                return True

def game_over(world: World):
    world.game_over.text = "GAME OVER"

def create_player() -> DesignerObject:
    """ Creates the player character """
    player = emoji("🏃")
    player.y = get_height()
    player.scale_x = 1.2
    player.scale_y = 1.2
    player.flip_x = True
    return player

def control_player_movement(world: World, key: str):
    if key == "right":
        move_player(world)
    if key == "left":
        move_player(world)

def move_player(world: World):
    global WORKER_SPEED
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        world.player_character.x -= WORKER_SPEED
        world.player_character.flip_x = False
    if keys[pygame.K_RIGHT]:
        world.player_character.x += WORKER_SPEED
        world.player_character.flip_x = True

def control_player_jump(world: World, key: str):
    if key == "space" and on_platform:
        player_jump(world, key)
    elif key == "space":
        player_jump(world, key)

def player_jump(world: World, key: str):
    global WORKER_HEIGHT, jumping, on_platform

    if key == "space" and not jumping:
        WORKER_HEIGHT = -20  # Jumping impulse
        jumping = True

    # Update player position
    world.player_character.y += WORKER_HEIGHT

    # Gravity
    if jumping:
        WORKER_HEIGHT += 1  # Gravity pulls the player down

    # Check if the player is on a platform
    for platform in world.platforms:
        if world.player_character.x >= platform.x and world.player_character.x <= platform.x + 300:
            if world.player_character.y >= platform.y - 3 and world.player_character.y <= platform.y + 3:
                jumping = False
                WORKER_HEIGHT = 0
                on_platform = True

    # Check if the player is on the ground
    if world.player_character.y >= get_height() - 20:
        world.player_character.y = get_height() - 20
        jumping = False
        WORKER_HEIGHT = 0

def player_border_stop(world: World):
    """ Stops player from going off screen """
    if world.player_character.x > get_width() - 5:
        world.player_character.x = get_width() - 18
    elif world.player_character.x < 5:
        world.player_character.x = 18
    if world.player_character.y < 20:
        world.player_character.y = 20
    elif world.player_character.y > get_height() - 20:
        world.player_character.y = get_height() - 20

#def run_game_timer():
#    global game_time
#    time.sleep(1)
#    game_time += 1
#    minutes = str(game_time // 60)
#    seconds = game_time % 60
#    if seconds < 10:
#        seconds = "0" + str(seconds)
#    return minutes + ":" + str(seconds)

#def update_game_timer(world: World):
#    with concurrent.futures.ThreadPoolExecutor() as game_timer:
#        game_timing = game_timer.submit(run_game_timer)
#        gaming_time = game_timing.result()
#        world.gaming_timer.text = gaming_time

when("starting", create_world)
when("typing", control_player_movement)
when("updating", move_player)
when("typing", control_player_jump)
when("updating", player_jump)
when("updating", player_border_stop)
when("updating", make_platforms)
when("updating", drop_platforms)
when("updating", destroy_platforms)
when("updating", make_obstacles)
when("updating", drop_obstacles)
when("updating", destroy_obstacles)
when("updating", player_on_platform)
#when("updating", update_game_timer)
when(collide_with_obstacle, game_over, pause)
start()
