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

iconImports = ["src/imagefiles/world_skills_feed.png", "src/imagefiles/input_skills_score.png", "src/imagefiles/analyze_skills.png", "src/imagefiles/autoGrant.png"]
worldSkillsIcon = pygame.image.load(iconImports[0])
inputSkillsIcon = pygame.image.load(iconImports[1])
analyzeSkillsIcon = pygame.image.load(iconImports[2])
autoGrantIcon = pygame.image.load(iconImports[3])
iconSize = 400

wsIconSize = iconSize * 0.4
worldSkillsIcon = pygame.transform.scale(worldSkillsIcon, (wsIconSize, wsIconSize)) # scales the images by a scale factor

isIconSize = iconSize * 0.25
inputSkillsIcon = pygame.transform.scale(inputSkillsIcon, (isIconSize, isIconSize)) # scales the images by a scale factor

pygame.display.set_caption("Skill-Issue v1.0.1") # Sets title of window
screen = pygame.display.set_mode(windowSize, pygame.FULLSCREEN) # Sets the dimensions of the window to the windowSize

font = pygame.font.Font(None, 36)

hdRatio = screenWidth / 1920

###### INITIALIZE ######

fps = 60
currentTime = 0
framerate = fps
clock = pygame.time.Clock()
page = "feed"
mode = "driver"

###### OBJECTS ######

debug = gui.Title(
    type="body",
    x=1920/2,
    y=20,
    text="FPS: " + str(framerate),
    textColor=(30,30,30),
    fontSize=15
    )

###### MAINLOOP ######

running = True # Runs the game loop
while running:
    framerate = round(1 / (time.time() - currentTime))
    currentTime = time.time()

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

    mainStruct.feedTab.moveTo(mainStruct.feedTab.x, mainStruct.feedTab.y)

    if mainStruct.feedTab.isClicked():
        page = "feed"
    if mainStruct.inputSkillsTab.isClicked():
        page = "input"
    if mainStruct.analyzeSkillsTab.isClicked():
        page = "analyze"
    if mainStruct.autoGrantTab.isClicked():
        page = "autoGrant"

    debug.setTitle("FPS: " + str(framerate))
    debug.draw(screen)

    if page == "feed":
        worldSkillsFeed.scrollWindow.draw(screen)
        worldSkillsFeed.worldSkillsTitle.draw(screen)
        worldSkillsFeed.dateUpdated.draw(screen)

        worldSkillsFeed.refreshFeed.draw(screen)
        worldSkillsFeed.exportList.draw(screen)

        screen.blit(worldSkillsIcon, (180 - wsIconSize/2, 280 - wsIconSize/2))

    elif page == "input":
        inputSkills.inputWindow.draw(screen)

        inputSkills.enterSkills.dynamicInteraction(pressedKey)
        inputSkills.enterSkills.draw(screen)
        inputSkills.inputSkillsTitle.draw(screen)

        screen.blit(inputSkillsIcon, (390 - isIconSize/2, 335 - isIconSize/2))

        inputSkills.progSkillsOption.draw(screen, mode=int(mode=="programming"))
        inputSkills.driverSkillsOption.draw(screen, mode=int(mode=="driver"))

        if inputSkills.progSkillsOption.isClicked():
            mode = "programming"
        elif inputSkills.driverSkillsOption.isClicked():
            mode = "driver"
            
    pygame.display.update()

# quit Pygame
pygame.quit()