import os
import random 
import math
import pygame

from os import listdir
from os.path import isfile, join

# Initializing pygame module
pygame.init()

# Setting caption at the top of the window
pygame.display.set_caption("Platformer") 

# Defining global variables
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

# Setting up mygame window
window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites): # This is the function that will flip our image
    return[pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2) # This is the path to the images we will be loading
    images = [f for f in listdir(path) if isfile(join(path, f))] # This loop will load every single file that is inside of these directories

    all_sprites = {} # This dictionary will have key value pairs. The key will be the animation style and the values will be all of the images in that animation

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha() # Here we are loading the image from path, appending the path to it, then get the transparent background

        sprites = []
        for i in range(sprite_sheet.get_width() // width): #  The width will be the width of an invidual image inside of the spritesheet
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height) # This is the location of our image in which we want to grab the new frame from
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface)) # We striped out the original frame and scaled then up

        if direction: # This if statement is saying; if you want a multi-directional animation, we need add these two keys to our directionary for every signle one of our animaations
            all_sprites[image.replace(".png", "") +"_right"] = sprites # this will strip off all .png name from our base image and append _right or _left
            all_sprites[image.replace(".png", "") +"_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block(size): # This function passes the size in which we want our block to be. Then we create an image of that size.
    path = join("assets", "Terrain", "Terrain.png") # This will find the block that we want in out Terrain folder
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size) # The image we want start is 96 pixels from the top of the screen. Here you pass the positionin which you want to load the image from, from the actual Terrain image
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite): # This class will inherit sprite from pygame because it makes it easy to do picture perfect collision
    COLOR = (255, 0, 0)
    GRAVITY = 1 # We are adding an acceleration for gravity. If you want the gravity to be faster you can increment this number
    SPRITES = load_sprite_sheets("MainCharacters", "PinkMan", 32, 32, True) # This will load the  MainCharacters dir and then the second dir will be the name of the character we want to load. We need to set the width and height to 32 and we are passing True becuase we want a multidirectional sprite
    ANIMATION_DELAY = 3 # This is going to account for the amount of delay between changing sprites

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height) # Rather than representing all of these values individually, we are going to put them on the rectangle which will make it easier for us to move the player around
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left" # We are adding this direction becuase we need to keep track of what direction theMaskDude Player is facing
        self.animation_count = 0 # We need to reset the count to change the animation frame
        self.fall_count = 0 # We need to keep track of how long we have been falling so that we know how quicly we should be accelerating downward 
        self.jump_count = 0 
 
    def jump(self):
        self.y_vel = -self.GRAVITY * 8 # We are multipling negative so that we jump UP in the air
        self.animation_count = 0
        self.jump_count += 1 # As soon as we jump we are getting rid of any gravity the character already obtained
        if self.jump_count == 1:
            self.fall_count = 0 # Then we will start applying gravity after we jump



    def move(self, dx, dy): # Adding move function which will take in the displacement of the x and y direction
        self.rect.x += dx # If we want to move up, down, left, right we just change the sign of dx and dy
        self.rect.y += dy

    def move_left(self, veL):
        self.x_vel = -veL # We are using negative velocity to move left which means we have to subtract from our x position
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, veL):
        self.x_vel = veL
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps): # This loop will be called once every frame (one itereation of the while loop). This will move our character in the correct direction
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY) # This will give us somewhat realistic fall of gravity
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0 # If we land we need to reset our gravity(fall_count)
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel += -1 # If we hit out head we want to reverse the velocity so that we move down

    def update_sprite(self): # This function will update our sprite. 
        sprite_sheet = "idle" # This the defualt sprite sheet
        if self.y_vel < 0:
            if self.jump_count == 1: # This is handling regular jump
                sprite_sheet = "jump"
            elif self.jump_count ==2: # This is handling double jump
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2: # This is handling the falling portion
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites) # Every 5 frames we want to show a different sprite in whatever animation we are using. For this we take the animation count, we divide it by 5, and then we mod whatever the len of our sprite is. Making this dynamic meaning it will work for any sprite
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
    
    def update(self): # This will update the rectangle that bounds our character based on the sprite that we are showing
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y)) # Depending on what sprite image we have, this will constantly adjust the rectangle (spec the width and height ). But we will use the same x and y position we have for this rectangle
        self.mask = pygame.mask.from_surface(self.sprite) # A mask is a mapping of all of the pixels that exist in the sprite

    def draw(self, win): # THis draw function wil draw the window, color, and rect
        win.blit(self.sprite, (self.rect.x, self.rect.y))

class Object(pygame.sprite.Sprite): # This will be a base class that we will use for all objects so that the collision will be uniform across all of them
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size) # Here we are getting the image that we need
        self.image.blit(block, (0, 0)) # Here we blit the image: which is a pygame surface
        self.mask = pygame.mask.from_surface(self.image)


def get_background(name): # Making function for background
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect() # This provides the x, y, width, and height of ("_, _," means we dont care about the x, y) 
    tiles = []

    # This loop provides is with how many tiles we need to create in the x and y direction
    for i in range(WIDTH // width + 1): # Integer diving this which tells us appox how many tiles you need x direction to fill the whole screen. To make sure there are no gaps we add 1 
        for j in range(HEIGHT // height + 1): # Same exact thing is done in the y direction
            pos = (i * width, j * height) # This is going to denote the position of the top left hand corner of the current tile we are adding to this tiles list. Changed to tuple directly
            tiles.append(pos)

    return tiles, image # We return the tiles and image so we can know what image we are going to use when we are drawing all these tiles


def draw(window, background, bg_image, player, objects):
    for tile in background: 
        window.blit(bg_image, tile) # This is where we draw the background: passing in the position in which we want to draW it at which is going to be 'tile'

    for obj in objects:
        obj.draw(window)

    player.draw(window)

    pygame.display.update() # We update the frame so that every single frame clears the screen

def handle_vertical_collision(player, objects, dy): # Adding collision
    collided_objects = []
    for obj in objects: # This will be all the objects we could be colliding with
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0: # If we are moving down on the screen 
                player.rect.bottom = obj.rect.top # We take to bottom of our player rectangle(players feet) and make it = to the top of the obj we are colliding with
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom # If we are moving up then we are hitting the bottom of an obj so we need to make the top = to the bottom
                player.hit_head()

        collided_objects.append(obj)

    return collided_objects

def handle_move(player, objects): # This function is in charge of moving player
    keys = pygame.key.get_pressed() # Checking if the keys on the keyboard are getting pressed

    player.x_vel = 0 # It's important to set the player velocity to zero to stay consistant with movement
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

    handle_vertical_collision(player, objects, player.y_vel)


def main(window): # Making the main function: We will run this to start the game
    clock = pygame.time.Clock()
    background, bg_image = get_background("Purple.png") # Adding background to main function

    block_size = 96

    player = Player(100, 100, 50, 50) # Adding player
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)] # This for loop will create blocks that go the left and to the right of the screen

    run = True   # This while loop will act as our event loop
    while run:
        clock.tick(FPS) # This ensures that our while loop is going to run no more than 60 FPS to regulate the frame rate across different devices
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # First event we will check for is if the user quit the game
                run = False
                break
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2: # This is to allow double jumping
                    player.jump()
        
        player.loop(FPS) # Need to call loop function becuase it is the function that actually moves the player
        handle_move(player, floor)
        draw(window, background, bg_image, player, floor)
             
    pygame.quit()
    quit()

# Purpose of this line in the function is to only call the main function if we run this file directly 
if __name__ == "__main__":
    main(window)