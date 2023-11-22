###### IMPORT ######

import pygame
import sys

import gui

###### SETUP ######

pygame.init()

screenInfo = pygame.display.Info()
screenWidth = screenInfo.current_w
screenHeight = screenInfo.current_h

###### OBJECTS ######
print("Generating inputSkills files...")

enterSkills = gui.Textbox(
    name="enter_skills",
    x=1920/2,
    y=1080/2 + 200,
    width=400,
    height=75,
    exampleText="Enter Skills Score",
    scale=1,
    fontSize=25
)

print("inputSkills files generated")