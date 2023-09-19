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
        self.x_vel = -vel # We are using negative velocity to move left which means we have to subtract from our x position
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, veL):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0


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


def draw(window, background, bg_image):
    for tile in background: 
        window.blit(bg_image, tile) # This is where we draw the background: passing in the position in which we want to draW it at which is going to be 'tile'

    pygame.display.update() # We update the frame so that every single frame clears the screen



# Making the main function: We will run this to start the game
def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Purple.png") # Adding backgrounf to main function

        # This while loop will act as our event loop
    run = True
    while run:
        clock.tick(FPS) # This ensures that our while loop is going to run no more than 60 FPS to regulate the frame rate across different devices
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # First event we will check for is if the user quit the game
                run = False
                break

        draw(window, background, bg_image)
             
    pygame.quit()
    quit()

# Purpose of this line in the function is to only call the main function if we run this file directly 
if __name__ == "__main__":
    main(window)