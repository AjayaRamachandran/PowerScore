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

pygame.display.set_caption("CustomCraft") # Sets title of window
screen = pygame.display.set_mode(windowSize, pygame.FULLSCREEN) # Sets the dimensions of the window to the windowSize

font = pygame.font.Font(None, 36)

###### INITIALIZE ######

fps = 60
clock = pygame.time.Clock()

#villagerProfessions = initializeVillagerProfessions()
#villagerBiomes = initializeVillagerBiomes()

namespace = "minecraft:" # if the namespace EVER needs to be changed for whatever reason (mods, resourcepacks, etc.) then this will keep that smooth

###### OBJECTS ######

createVillagerButton = gui.Button(
    name="create_villager",
    width=450,
    height=75,
    cornerRadius = 15,
    color=[50, 150, 50],
    text="CREATE VILLAGER",
    x=screenWidth/2,
    y=screenHeight/2,
    scale=1,
    fontSize=25
    )

createItemButton = gui.Button(
    name="create_item",
    width=450,
    height=75,
    cornerRadius=15,
    color=[50, 150, 50],
    text="CREATE ITEM",
    x=screenWidth/2,
    y=screenHeight/2 + 100,
    scale=1,
    fontSize=25
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

    createVillagerButton.draw(screen, borderSize=3)
    createItemButton.draw(screen, borderSize=3)
    

    pygame.display.update()

# quit Pygame
pygame.quit()