###### IMPORT ######

import pygame
from PIL import Image
import io

import random
from math import *
import numpy as np

import time

import gui
from objects import mainStruct

###### SETUP ######

pygame.init()

screenInfo = pygame.display.Info()
screenWidth = screenInfo.current_w
screenHeight = screenInfo.current_h

windowSize = (screenWidth, screenHeight)

bgPhoto = "bg.jpg"
bg = pygame.image.load(bgPhoto)
bg_rect = bg.get_rect()

pygame.display.set_caption("Skill-Issue v1.0.1") # Sets title of window
screen = pygame.display.set_mode(windowSize, pygame.FULLSCREEN) # Sets the dimensions of the window to the windowSize

font = pygame.font.Font(None, 36)

###### INITIALIZE ######

fps = 60
clock = pygame.time.Clock()

###### OBJECTS ######


###### MAINLOOP ######

running = True # Runs the game loop
while running:
    screen.fill((30, 30, 37))

    for event in pygame.event.get(): # checks if program is quit, if so stops the code
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    # runs framerate wait time
    clock.tick(fps)
    # update the screen
    screen.blit(bg, bg_rect)

    mainStruct.starterWindow.draw(screen)
    mainStruct.feedTab.draw(screen)
    mainStruct.inputSkillsTab.draw(screen)
    mainStruct.analyzeSkillsTab.draw(screen)
    mainStruct.autoGrantTab.draw(screen)
    mainStruct.mainTitle.draw(screen)
    mainStruct.mainSubtitle.draw(screen)

    pygame.display.update()

# quit Pygame
pygame.quit()