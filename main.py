from designer import *
from dataclasses import dataclass
from random import randint
import pygame


#Determines player character speed
Worker_Speed = 10

#Determines player character jump height
Worker_Height = 0

#Jumping Variable
jumping = False

#Determines how fast obstacles fall
Obstacles_fall_speed = 5

#Sets background image
background_image("https://www.thomsonreuters.com/en-us/posts/wp-content/uploads/sites/20/2016/04/open-floor-plan-office-800x450.jpg")

@dataclass
class World:
    player_character: DesignerObject
    obstacles: list[DesignerObject]

def create_world() -> World:
    """ Creates the game world """
    return World(create_player(), [])

def create_ground() -> DesignerObject:
    """ Creates starting point for character """

    lines = line("black", 0,get_height()-Worker_Height,get_width(),get_height()-Worker_Height,2)
    return lines

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
def collide_with_obstacle(world: World):
    for obstacle in world.obstacles:
        if colliding(obstacle, world.player_character):
            return True

def game_over(world: World):
    world.text = "GAME OVER"

def create_player() -> DesignerObject:
    """ Creates the player character """
    player = emoji("🏃")
    player.y = get_height() - 25
    player.flip_x = True
    return player

def control_player_movement(world: World, key: str):
    if key == "right":
        move_player(world)
    if key == "left":
        move_player(world)

def move_player(world: World):
    global Worker_Speed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        world.player_character.x -= Worker_Speed
        world.player_character.flip_x = False
    if keys[pygame.K_RIGHT]:
        world.player_character.x += Worker_Speed
        world.player_character.flip_x = True

def control_player_jump(world: World, key: str):
    if key == "space":
        player_jump(world, key)

def player_jump(world: World, key: str):
    global Worker_Height, jumping

    if key == "space" and not jumping:
        Worker_Height = -20  # Jumping impulse
        jumping = True

    # Update player position
    world.player_character.y += Worker_Height

    # Gravity
    if jumping:
        Worker_Height += 1  # Gravity pulls the player down

    # Check if the player is on the ground
    if world.player_character.y >= get_height() - 18:
        world.player_character.y = get_height() - 18
        jumping = False
        Worker_Height = 0

def player_border_stop(world: World):
    """ Stops player from going off screen """
    if world.player_character.x > get_width() - 5:
        world.player_character.x = get_width() - 18
    elif world.player_character.x < 5:
        world.player_character.x = 18
    if world.player_character.y < 20:
        world.player_character.y = 20
    elif world.player_character.y > get_height() - 18:
        world.player_character.y = get_height() - 18


when("starting", create_world)
when("typing", control_player_movement)
when("updating", move_player)
when("typing", control_player_jump)
when("updating", player_jump)
when("updating", player_border_stop)
when("updating", make_obstacles)
when("updating", drop_obstacles)
when("updating", destroy_obstacles)
when(collide_with_obstacle, game_over, pause)
start()