from designer import *

from dataclasses import dataclass

#Determines player character speed
Worker_Speed = 5

#Determines player character jump height
Worker_Height = 50

@dataclass
class World:
    player_character: DesignerObject
    player_speed: int
    building: DesignerObject

def create_world() -> World:
    """ Creates the game world """
    return World(create_player(), Worker_Speed, create_lines())
def create_lines() -> DesignerObject:
    lines = line("black", 0,get_height()-Worker_Height,get_width(),get_height()-Worker_Height,2)
    return lines


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

def player_border_stop(world: World):
    """ Stops player from going off screen """
    if world.player_character.x > get_width() - 5:
        move_player_left(world)
    elif world.player_character.x < 5:
        move_player_right(world)
    if world.player_character.y < 20:
        world.player_character.y = 20

when("starting", create_world)
when("updating", move_player_horizontal)
when("typing", control_player_horizontal)
when("typing", control_player_jump)
when("updating", player_border_stop)
start()