###### IMPORT ######

import pygame
from PIL import Image
import io

import random
from math import *
import numpy as np

import time

import gui

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

enterSkills = gui.Button(
    name="enter_skills",
    width=450,
    height=75,
    cornerRadius = 15,
    color=[180, 180, 180],
    text="ENTER SKILLS SCORE",
    x=screenWidth/2,
    y=screenHeight/2,
    scale=1,
    fontSize=25
    )

analyzeSkills = gui.Button(
    name="analyze_skills",
    width=450,
    height=75,
    cornerRadius=15,
    color=[200, 30, 30],
    text="ANALYZE SCORES",
    x=screenWidth/2,
    y=screenHeight/2 + 100,
    scale=1,
    fontSize=25
    )

mainTitle = gui.Title(
    type="title",
    x=screenWidth/2,
    y=screenHeight/2 - 300,
    text="Skill Issue",
    textColor=(30,30,30),
    fontSize=100
    )

mainSubtitle = gui.Title(
    type="title",
    x=screenWidth/2,
    y=screenHeight/2 - 220,
    text="The VRC Skills Copilot",
    textColor=(30,30,30),
    fontSize=50
    )

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

    enterSkills.draw(screen, borderSize=3)
    analyzeSkills.draw(screen, borderSize=3)
    mainTitle.draw(screen)
    mainSubtitle.draw(screen)

    #mainTitle.moveTo(random.randint(-100, 100), random.randint(-100, 100))
    

    pygame.display.update()

# quit Pygame
pygame.quit()