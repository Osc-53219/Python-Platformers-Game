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