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
    x=385,
    y=1080/2 - 100,
    width=480,
    height=60,
    exampleText="(ex. 145)",
    scale=1,
    fontSize=25,
    characterLimit=3
)

inputSkillsTitle = gui.Title(
    type="title",
    x=380,
    y=1080/2 - 300,
    text="Input a Skills Score",
    textColor=(30,30,30),
    fontSize=45
    )

progSkillsOption = gui.Button(
    name="programming_skills_option",
    width=225,
    height=50,
    cornerRadius = 15,
    color=[50, 50, 50],
    text="Programming",
    x=260,
    y=520,
    scale=1,
    fontSize=20
    )

driverSkillsOption = gui.Button(
    name="driver_skills_option",
    width=225,
    height=50,
    cornerRadius = 15,
    color=[50, 50, 50],
    text="Driver",
    x=510,
    y=520,
    scale=1,
    fontSize=20
    )

inputWindow = gui.Window(
    name="input_window",
    width=600,
    height=800,
    cornerRadius = 15,
    color=[180, 180, 180],
    x=385,
    y=1080/2 + 50,
    scale=1,
    )

print("inputSkills files generated")