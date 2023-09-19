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
BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

# Setting up mygame window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Making function for background: 
def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect() # This provides the x, y, width, and height of ("_, _," means we dont care about the x, y) 
    tiles = []

    # This loop provides is with how many tiles we need to create in the x and y direction
    for i in range(WIDTH // width + 1): # Integer diving this which tells us appox how many tiles you need x direction to fill the whole screen. To make sure there are no gaps we add 1 
        for j in range(HEIGHT // height + 1): # Same exact thing is done in the y direction
            pos = [i * width, j * height] # This is going to denote the position of the top left hand corner of the current tile we are adding to this tiles list
            tiles.append(pos)

    return tiles, image # We return the tiles and image so we can know what image we are going to use when we are drawing all these tiles



# Making the main function: We will run this to start the game
def main(window):
    clock = pygame.time.Clock()

        # This while loop will act as our event loop
    run = True
    while run:
        clock.tick(FPS) # This ensures that our while loop is going to run no more than 60 FPS to regulate the frame rate across different devices
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # First event we will check for is if the user quit the game
                run = False
                break
             
    pygame.quit()
    quit()

# Purpose of this line in the function is to only call the main function if we run this file directly 
if __name__ == "__main__":
    main(window)