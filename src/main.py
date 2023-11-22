###### IMPORT ######

import pygame

import random
from math import *
import numpy as np

import time

import gui
from objects import mainStruct
from objects import worldSkillsFeed
from objects import inputSkills

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

hdRatio = screenWidth / 1920

###### INITIALIZE ######

fps = 60
clock = pygame.time.Clock()
page = "feed"

###### OBJECTS ######

debug = gui.Title(
    type="body",
    x=1920/2,
    y=20,
    text="Page: " + page,
    textColor=(30,30,30),
    fontSize=15
    )

###### MAINLOOP ######

running = True # Runs the game loop
while running:
    screen.fill((30, 30, 37))
    pressedKey = ""

    for event in pygame.event.get(): # checks if program is quit, if so stops the code
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                pressedKey = "keyBKSPC"
            else:
                pressedKey = event.unicode
    # runs framerate wait time
    clock.tick(fps)
    # update the screen
    screen.blit(bg, bg_rect)

    mainStruct.starterWindow.draw(screen)
    mainStruct.feedTab.draw(screen, mode=int(page=="feed"))
    mainStruct.inputSkillsTab.draw(screen, mode=int(page=="input"))
    mainStruct.analyzeSkillsTab.draw(screen, mode=int(page=="analyze"))
    mainStruct.autoGrantTab.draw(screen, mode=int(page=="autoGrant"))

    worldSkillsFeed.scrollWindow.draw(screen)

    worldSkillsFeed.mainTitle.draw(screen)
    worldSkillsFeed.mainSubtitle.draw(screen)

    if mainStruct.feedTab.isClicked():
        page = "feed"
    if mainStruct.inputSkillsTab.isClicked():
        page = "input"
    if mainStruct.analyzeSkillsTab.isClicked():
        page = "analyze"
    if mainStruct.autoGrantTab.isClicked():
        page = "autoGrant"

    debug.setTitle("Page: " + page)
    debug.draw(screen)

    inputSkills.enterSkills.dynamicInteraction(pressedKey)
    inputSkills.enterSkills.draw(screen)

    pygame.display.update()

# quit Pygame
pygame.quit()