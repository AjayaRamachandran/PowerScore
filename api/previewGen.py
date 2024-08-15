###### IMPORT ######
from math import *
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
import base64
from datetime import datetime
from PIL import Image
from openpyxl import Workbook
from io import BytesIO

###### OPERATOR FUNCTIONS ######
def getDays(date):
    monthLengths = [31,28,31,30,31,30,31,31,30,31,30,31]
    return int(date[:4]) * 365 + sum(monthLengths[:int(date[5:7]) - 1]) + int(date[8:])

def setLength(value, numDigits):
    zeroString = ""
    if len(str(value)) < numDigits:
        for i in range(numDigits - len(str(value))):
            zeroString = zeroString + "0"
    return zeroString + str(value)

def createImage(num):
    pygame.init()
    windowSize = [530, 250]
    width = windowSize[0] + 100
    height = windowSize[1]

    screen = pygame.display.set_mode(windowSize)

    font = pygame.font.Font("Teko-Bold.ttf", 250)
    cyan = (14, 97, 114)
    screen.fill(cyan)

    textCenter = [width / 4, height/2 + 20]
    badgeCenter = [windowSize[0] * 3 / 4 + 10, height/2]

    text = font.render(str(num), True, (255,255,255))
    textRect = [textCenter[0] - text.get_rect()[2]/2, textCenter[1] - text.get_rect()[3]/2, text.get_rect()[2], text.get_rect()[3]]
    screen.blit(text, textRect)

    rank = giveRanking(num)
    rankCopy = rank.replace(" ", "")
    badgeFileDir = "newbadges/" + rankCopy + ".png"

    badge = pygame.image.load(badgeFileDir)
    badge = pygame.transform.scale(badge, (250, 250))
    badgeRect = [badgeCenter[0] - badge.get_rect()[2]/2, badgeCenter[1] - badge.get_rect()[3]/2, badge.get_rect()[2], badge.get_rect()[3]]
    screen.blit(badge, badgeRect)


    pygame.image.save(screen, f"api/previews/{num}.jpg")

    




###### RANKING ######

ranking = [
    ["Bronze I", 0],
    ["Bronze II", 11],
    ["Bronze III", 21],

    ["Silver I", 31],
    ["Silver II", 38],
    ["Silver III", 44],

    ["Gold I", 51],
    ["Gold II", 58],
    ["Gold III", 64],

    ["Diamond I", 71],
    ["Diamond II", 74],
    ["Diamond III", 78],

    ["Royal I", 81],
    ["Royal II", 84],
    ["Royal III", 88],

    ["Ethereal I", 91],
    ["Ethereal II", 94],
    ["Ethereal III", 97],
    ["Upper Limit", 100]
]

def giveRanking(value): # function to get the rank given a powerscore
    index = 0
    while ranking[index][1] < value:
        index += 1
    index -= 1
    return ranking[index][0]

###### MAIN ######

for i in range(1, 101):
    #createImage(i)
    print('{"' + str(i) + '" : ""},')