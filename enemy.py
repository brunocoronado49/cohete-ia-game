import pygame
from constants import *
import random
import globals


ORIGINAL_SIZE = (60.154)
MIN_WIDTH = 15
MAX_WIDTH = 25

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()