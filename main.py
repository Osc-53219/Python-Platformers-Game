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

# This class will inherit sprite from pygame because it makes it easy to do picture perfect collision
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height) # Rather than representing all of these values individually, we are going to put them on the rectangle which will make it easier for us to move the player around
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left" # We are adding this direction becuase we need to keep track of what direction the Player is facing
        self.animation_count = 0 # We need to reset the count to change the animation frame

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
        self.move(self.x_vel, self.y_vel)

    def draw(self, win): # THis draw function wil draw the window, color, and rect
        pygame.draw.rect(win, self.COLOR, self.rect)



# Making function for background: 
def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect() # This provides the x, y, width, and height of ("_, _," means we dont care about the x, y) 
    tiles = []

    # This loop provides is with how many tiles we need to create in the x and y direction
    for i in range(WIDTH // width + 1): # Integer diving this which tells us appox how many tiles you need x direction to fill the whole screen. To make sure there are no gaps we add 1 
        for j in range(HEIGHT // height + 1): # Same exact thing is done in the y direction
            pos = (i * width, j * height) # This is going to denote the position of the top left hand corner of the current tile we are adding to this tiles list. Changed to tuple directly
            tiles.append(pos)

    return tiles, image # We return the tiles and image so we can know what image we are going to use when we are drawing all these tiles


def draw(window, background, bg_image, player):
    for tile in background: 
        window.blit(bg_image, tile) # This is where we draw the background: passing in the position in which we want to draW it at which is going to be 'tile'

    player.draw(window)

    pygame.display.update() # We update the frame so that every single frame clears the screen


def handle_move(player): # This function is in charge of moving player
    keys = pygame.key.get_pressed() # Checking if the keys on the keyboard are getting pressed

    player.x_vel = 0 # It's important to set the player velocity to zero to stay consistant with movement
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)


def main(window): # Making the main function: We will run this to start the game
    clock = pygame.time.Clock()
    background, bg_image = get_background("Purple.png") # Adding background to main function

    player = Player(100, 100, 50, 50) # Adding player

    run = True   # This while loop will act as our event loop
    while run:
        clock.tick(FPS) # This ensures that our while loop is going to run no more than 60 FPS to regulate the frame rate across different devices
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # First event we will check for is if the user quit the game
                run = False
                break
        
        player.loop(FPS) # Need to call loop function becuase it is the function that actually moves the player
        handle_move(player)
        draw(window, background, bg_image, player)
             
    pygame.quit()
    quit()

# Purpose of this line in the function is to only call the main function if we run this file directly 
if __name__ == "__main__":
    main(window)