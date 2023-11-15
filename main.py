from designer import *
from dataclasses import dataclass
import pygame

#Determines player character speed
Worker_Speed = 10

#Determines player character jump height
Worker_Height = 0

#Jumping Variable
jumping = False

#Sets background image
background_image("https://www.thomsonreuters.com/en-us/posts/wp-content/uploads/sites/20/2016/04/open-floor-plan-office-800x450.jpg")

@dataclass
class World:
    player_character: DesignerObject
    ground: DesignerObject

def create_world() -> World:
    """ Creates the game world """
    return World(create_player(), create_ground())

def create_ground() -> DesignerObject:
    """ Creates starting point for character """
    ground = rectangle("darkgray", get_width() + get_width() + 40, 15, -20, get_height())
    return ground

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

def player_ground_check(world: World):
    """ Checks if player is on ground """
    if colliding(world.player_character, world.ground):
        world.player_character.y = world.ground.y - 25

when("starting", create_world)
when("typing", control_player_movement)
when("updating", move_player)
when("typing", control_player_jump)
when("updating", player_jump)
when("updating", player_border_stop)
when("updating", player_ground_check)
start()