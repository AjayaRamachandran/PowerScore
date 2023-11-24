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
print("Generating worldSkillsFeed files...")

worldSkillsTitle = gui.Title(
    type="title",
    x=360,
    y=1080/2 - 300,
    text="World Skills Feed",
    textColor=(30,30,30),
    fontSize=60
    )

dateUpdated = gui.Title(
    type="title",
    x=300,
    y=1080/2 - 230,
    text="Last Updated: 11/22/2023",
    textColor=(30,30,30),
    fontSize=30
    )

scrollWindow = gui.Window(
    name="scroll_window",
    width=1000,
    height=800,
    cornerRadius = 15,
    color=[180, 180, 180],
    x=1920/2 + 375,
    y=1080/2 + 50,
    scale=1,
    )

print("worldSkillsFeed files generated")