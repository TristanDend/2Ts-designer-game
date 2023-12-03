from designer import *
from dataclasses import dataclass
from random import randint
import pygame

@dataclass
class World:
    game_over: DesignerObject
    game_timer: DesignerObject
    frame_timer: int
    player_character: DesignerObject
    obstacles: list[DesignerObject]
    platforms: list[DesignerObject]
    floor_exists: bool
    on_platform: bool
    RUN_SPEED: int
    JUMP_HEIGHT: int
    jumping: bool
    PLATFORM_SPEED: int
    game_time: int
    OBSTACLE_SPEED: int
    fall_rate: int
    FALL_SPEED: int
    platform_count: int

def create_world() -> World:
    """ Creates the game world """
    return World(text("red", "", 30),
                 text("black", "0:00", 20, 25, 20),
                 0, create_player(), [], [], True, False, 10, 0, False, 3, 0, 5, 75, 0, 0)

def create_platforms() -> DesignerObject:
    """ Creates platforms for the player """
    platform = line("black", -1, -5, get_width() + 1, -5, 3)
    return platform

def make_platforms(world: World):
    if world.frame_timer % 60 == 0:
        world.platforms.append(create_platforms())

def drop_platforms(world: World):
    for platform in world.platforms:
        platform.y += world.PLATFORM_SPEED

def teleport_platform(world: World):
    try:
        if world.platforms[world.platform_count].y > get_height() + 2 and world.frame_timer % 60 == 0:
            world.platforms[world.platform_count].y = -180
            world.on_platform = False
    except:
        pass

def player_on_platform(world: World):
    try:
        if world.player_character.y >= world.platforms[world.platform_count].y - 20 and world.player_character.y <= world.platforms[world.platform_count].y:
            world.on_platform = True
            cool_variable = world.platform_count
            world.platform_count = cool_variable + 1
    except:
        pass

def create_obstacles() -> DesignerObject:
    """ Creates obstacles for the player """
    obstacle = emoji("🔻")
    obstacle.scale_x = 1.5
    obstacle.scale_y = 1.5
    obstacle.x = randint(0, get_width())
    obstacle.y = 0
    return obstacle

def make_obstacles(world: World):
    cap_obstacles = len(world.obstacles) < 11
    random_chance = randint(1, world.fall_rate) == 50
    if cap_obstacles and random_chance:
        world.obstacles.append(create_obstacles())

def drop_obstacles(world: World):
    for obstacle in world.obstacles:
        obstacle.y += world.OBSTACLE_SPEED

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
    world.game_timer.text = "Your time was " + world.game_timer.text
    world.game_timer.text_size = 30
    world.game_timer.x = world.game_over.x
    world.game_timer.y = world.game_over.y + 30
    world.game_timer.color = "red"

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
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        world.player_character.x -= world.RUN_SPEED
        world.player_character.flip_x = False
    if keys[pygame.K_RIGHT]:
        world.player_character.x += world.RUN_SPEED
        world.player_character.flip_x = True

def control_player_jump(world: World, key: str):
    if key == "space":
        player_jump(world, key)

def player_jump(world: World, key: str):
    if key == "space" and not world.jumping:
        world.JUMP_HEIGHT = -20
        world.jumping = True

    # Update player position
    world.player_character.y += world.JUMP_HEIGHT

    # Starts pulling player down
    if world.jumping:
        world.JUMP_HEIGHT += 1

    # Check if the player is on a platform
    try:
        if colliding(world.player_character, world.platforms[world.platform_count]):#world.player_character.y >= world.platforms[world.platform_count].y - 20 and world.player_character.y <= world.platforms[world.platform_count].y:
            world.jumping = False
            world.JUMP_HEIGHT = 0
            world.on_platform = True
            world.floor_exists = False
    except:
        pass

    # Check if the player is on the ground
    if world.player_character.y >= get_height() - 20:
        world.jumping = False
        world.JUMP_HEIGHT = 0

def player_while_on_platform(world: World):
    try:
        if world.on_platform:
            world.player_character.y = world.platforms[world.platform_count].y - 20
            cool_variable = world.platform_count
            if world.jumping:
                world.on_platform = False
                world.platform_count = cool_variable + 1
    except:
        pass

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

def surviving_longer(world: World) -> bool:
    if world.game_time > 5:
        return True

def increase_difficulty(world: World):
    world.fall_rate = 50

def count_time(world: World):
    world.frame_timer += 1
    if world.frame_timer % 30 == 0:
        world.game_time += 1
        minutes = str(world.game_time // 60)
        seconds = world.game_time % 60
        if seconds < 10:
            seconds = "0" + str(seconds)
        world.game_timer.text = minutes + ":" + str(seconds)

def floor_removal(world: World) -> bool:
    if not world.floor_exists:
        if world.player_character.y > get_height() - 23:
            return True

when("starting", create_world)
when("typing", control_player_movement)
when("updating", move_player)
when("typing", control_player_jump)
when("updating", player_jump)
when("updating", player_border_stop)
when("updating", make_platforms)
when("updating", drop_platforms)
when("updating", teleport_platform)
when("updating", make_obstacles)
when("updating", drop_obstacles)
when("updating", destroy_obstacles)
when("updating", player_on_platform)
when("updating", player_while_on_platform)
when("updating", count_time)
when(collide_with_obstacle, game_over, pause)
when(floor_removal, game_over, pause)
when(surviving_longer, increase_difficulty)
start()