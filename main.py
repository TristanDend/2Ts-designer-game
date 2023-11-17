from designer import *
from dataclasses import dataclass
from random import randint

#Determines player character speed
Worker_Speed = 5

#Determines player character jump height
Worker_Height = 50

#Determines how fast obstacles fall
Obstacles_fall_speed = 5

#Sets background image
background_image("https://www.thomsonreuters.com/en-us/posts/wp-content/uploads/sites/20/2016/04/open-floor-plan-office-800x450.jpg")

@dataclass
class World:
    player_character: DesignerObject
    player_speed: int
    building: DesignerObject
    obstacles: list[DesignerObject]

def create_world() -> World:
    """ Creates the game world """
    return World(create_player(), Worker_Speed, create_lines(), [])

def create_lines() -> DesignerObject:
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
    player.y = get_height() - 18
    player.flip_x = True
    return player

def move_player_horizontal(world: World):
    """ Moves player on the x axis """
    world.player_character.x += world.player_speed

def move_player_left(world: World):
    """ Moves player left """
    world.player_speed = -Worker_Speed
    world.player_character.flip_x = False

def move_player_right(world: World):
    """ Moves player right """
    world.player_speed = Worker_Speed
    world.player_character.flip_x = True

def player_jump(world: World):
    """ Allows player to jump """
    world.player_character.y -= Worker_Height

def player_down(world: World):
    """ Allows player to fall """
    world.player_character.y += Worker_Height

def control_player_horizontal(world: World, key: str):
    """ Player controls character moving left and right """
    if key == "left":
        move_player_left(world)
    elif key == "right":
        move_player_right(world)

def control_player_jump(world: World, key: str):
    """ Player controls character jump """
    if key == "space":
        player_jump(world)

def control_player_down(world: World, key: str):
    """ Controls player to go down"""
    if key == "down":
        player_down(world)
def player_border_stop(world: World):
    """ Stops player from going off screen """
    if world.player_character.x > get_width() - 5:
        move_player_left(world)
    elif world.player_character.x < 5:
        move_player_right(world)
    if world.player_character.y < 20:
        world.player_character.y = 20
    elif world.player_character.y > get_height() - 18:
        world.player_character.y = get_height() - 18

when("starting", create_world)
when("updating", move_player_horizontal)
when("typing", control_player_horizontal)
when("typing", control_player_jump)
when("updating", player_border_stop)
when("typing", control_player_down)
when("updating", make_obstacles)
when("updating", drop_obstacles)
when("updating", destroy_obstacles)
when(collide_with_obstacle, game_over, pause)
start()