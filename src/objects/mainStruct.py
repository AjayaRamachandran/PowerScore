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
print("Generating mainStruct files...")

starterWindow = gui.Window(
    name="opening_window",
    width=1800,
    height=850,
    cornerRadius = 15,
    color=[180, 180, 180],
    x=screenWidth/2,
    y=screenHeight/2 + 50,
    scale=1,
    )

feedTab = gui.Button(
    name="feed_tab",
    width=426,
    height=75,
    cornerRadius = 15,
    color=[80, 120, 120],
    text="World Skills Feed",
    x=273,
    y=100,
    scale=1,
    fontSize=20
    )

inputSkillsTab = gui.Button(
    name="input_skills_tab",
    width=426,
    height=75,
    cornerRadius = 15,
    color=[80, 120, 120],
    text="Input Skills Score",
    x=731,
    y=100,
    scale=1,
    fontSize=20
    )

analyzeSkillsTab = gui.Button(
    name="analyze_score_tab",
    width=426,
    height=75,
    cornerRadius = 15,
    color=[80, 120, 120],
    text="Analyze Skills",
    x=1189,
    y=100,
    scale=1,
    fontSize=20
    )

autoGrantTab = gui.Button(
    name="autoGrant_tab",
    width=426,
    height=75,
    cornerRadius = 15,
    color=[80, 120, 120],
    text="AutoGrant",
    x=1647,
    y=100,
    scale=1,
    fontSize=20
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

enterSkills = gui.Textbox(
    name="enter_skills",
    x=screenWidth/2,
    y=screenHeight/2 + 200,
    width=400,
    height=100,
    exampleText="Enter Skills Score",
    scale=1,
    fontSize=30
)

print("mainStruct files generated")