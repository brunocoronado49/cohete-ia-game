import pygame
from constants import *
from player import Player
from pygame.locals import *
from webcam import Webcam
from enemy import Enemy
from events import *
from background import Background
import globals
import random

import cv2
import mediapipe as mp
import math


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        self.running = True
        self.started = False
        
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_styles
        
        pygame.init()
        pygame.display.set_caption("Aliens")
        
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.smaller_font = pygame.font.Font('freesansbold.ttf', 22)
        self.background = Background()
        
        self.initialize()
        
    def initialize(self):
        self.start_time = pygame.time.get_ticks()
        self.last_frame_time = self.start_time
        self.player = Player()
        self.movement = 0
        
        self.enemy_timer = 1000
        pygame.time.set_timer(ADD_ENEMY, self.enemy_timer)
        
        self.enemies = pygame.sprite.Group()
        
        self.lost = False
        self.score = 0
        
        self.webcam = Webcam().start()
        
        self.max_face_surf_height = 0
        self.face_left_x = 0
        self.face_right_x = 0
        self.face_top_y = 0
        self.face_bottom_y = 0
        
    def update(self, delta_time):
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
        
        if self.lost or not self.started:
            for event in events:
                if event.type == KEYDOWN and event.key == K_RETURN:
                    self.initialize()
                    self.started = True
        else:
            globals.game_speed = 1 + ((pygame.time.get_ticks() - self.start_time) / 1000) * .1
            self.score = self.score + (delta_time * globals.game_speed)
            
            for event in events:
                if event.type == ADD_ENEMY:
                    num = random.randint(1, 2)
                    for e in range(num):
                        enemy = Enemy()
                        self.enemies.add(enemy)
                        
                    self.enemy_timer = 1000 - ((globals.game_speed - 1) * 100)
                    if self.enemy_timer < 50: self.enemy_timer = 50
                    pygame.time.set_timer(ADD_ENEMY, int(self.enemy_timer))
            
            