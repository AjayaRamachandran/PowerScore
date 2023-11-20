###### IMPORT ######

from PIL import Image
import io
import pygame

import random
from math import *

from tkinter.filedialog import asksaveasfile

###### SETUP ######

pygame.init()
screenInfo = pygame.display.Info()
screenWidth = screenInfo.current_w
screenHeight = screenInfo.current_h

###### FUNCTIONS ######

def createSamplePixelArray(height, width): # test function
    array = []
    for h in range(height):
        row = []
        for w in range(width):
            row.append([random.randint(0,255), random.randint(0,255), random.randint(0,255), 255])
        array.append(row)
    return array

def createButton(width, height, color, x, y, scale, type): # runs function to generate a button image based on some basic rules
    cornerRadius = 10
    array = []
    for w in range(width):
        row = []
        for h in range(height):
            if type == 0 or type == 1:
                dimFactor = 1 - (type == 1)*0.2

                outerRadius = cornerRadius**2 + 5
                innerRadius = cornerRadius**2 - 5

                outOfRadius = False
                antiAliased = False

                if w < cornerRadius and h < cornerRadius:
                    outOfRadius = (cornerRadius - w)**2 + (cornerRadius - h)**2 > cornerRadius**2 + 1
                    antiAliased = innerRadius < (cornerRadius - w)**2 + (cornerRadius - h)**2 < outerRadius
                elif w > width - cornerRadius and h > height - cornerRadius:
                    outOfRadius = (width - w - cornerRadius)**2 + (height - w - cornerRadius)**2 > cornerRadius**2 + 1
                    antiAliased = innerRadius < (cornerRadius - w)**2 + (cornerRadius - h)**2 < outerRadius

                if outOfRadius:
                    row.append([0,0,0,0])
                elif antiAliased:
                    row.append([int(color[0]/dimFactor),int(color[1]/dimFactor),int(color[2]/dimFactor),125])
                else:
                    row.append([int(color[0]/dimFactor),int(color[1]/dimFactor),int(color[2]/dimFactor),255])

                
            
        array.append(row)
    return array

def spawnButton(width, height, color, x, y, scale, names):
    for type in range(4): # generates images of all the different states the button could be in
        image = Image.new("RGBA", (width, height))
        for x, row in enumerate(createButton(width, height, color, x, y, scale, type)):
            for y, pixel in enumerate(row):
                image.putpixel((x, y), tuple(pixel))

        image.save(names[type])

###### CLASSES ######
class Button:
    def __init__(self, name, x, y, width, height, cornerRadius, color, text, scale, fontSize=20):
        #---SELF PROPERTIES---#
        ## Essential/Very Important ##
        self.name = name
        self.rect = pygame.Rect(x-width*scale/2, y-height*scale/2, width*scale, height*scale)
        self.x = x
        self.y = y

        ## Visual Info (Cosmetic) ##
        self.color = color
        self.text = text

        ## Visual Info (Spatial) ##
        self.width = width
        self.height = height
        self.scale = scale

        ## Text Attributes ##
        self.font = pygame.font.Font("fonts/Inter-Regular.ttf", fontSize)
        self.textColor = (255, 255, 255)  # Default text color
        self.fontSize = fontSize

        ## File Saving ##
        self.fileNames = ["images/base_" + str(name) + ".png",
                          "images/dimmed_" + str(name) + ".png",
                          "images/black_" + str(name) + ".png",
                          "images/white_" + str(name) + ".png"]

        #---INITIAL FUNCTIONS/SCRIPTS---#
        spawnButton(width=width, height=height, color=self.color, x=x, y=y, scale=scale, names=self.fileNames)

    def draw(self, screen, borderSize=3):
        button = pygame.image.load(self.fileNames[0]) # loads images of all the different states the button could be in
        dimmedButton = pygame.image.load(self.fileNames[1])
        blackButton = pygame.image.load(self.fileNames[2])
        whiteButton = pygame.image.load(self.fileNames[3])

        button = pygame.transform.scale(button, (self.width * self.scale, self.height * self.scale)) # scales the images by a scale factor (for the "pixelated" look)
        dimmedButton = pygame.transform.scale(dimmedButton, (self.width * self.scale, self.height * self.scale))
        blackButton = pygame.transform.scale(blackButton, (self.width * self.scale, self.height * self.scale))
        whiteButton = pygame.transform.scale(whiteButton, (self.width * self.scale, self.height * self.scale))

        screen.blit(blackButton, (self.x - self.width*self.scale/2 - borderSize, self.y - self.height*self.scale/2 - borderSize)) # draws a black border around the button of a specific thickness
        screen.blit(blackButton, (self.x - self.width*self.scale/2 + borderSize, self.y - self.height*self.scale/2 - borderSize))
        screen.blit(blackButton, (self.x - self.width*self.scale/2 - borderSize, self.y - self.height*self.scale/2 + borderSize))
        screen.blit(blackButton, (self.x - self.width*self.scale/2 + borderSize, self.y - self.height*self.scale/2 + borderSize))

        if self.rect.collidepoint(pygame.mouse.get_pos()): # blits to screen the dimmed version of the button if the mouse is hovering over it
            screen.blit(dimmedButton, (self.x - self.width*self.scale/2, self.y - self.height*self.scale/2))
        else:
            screen.blit(button, (self.x - self.width*self.scale/2, self.y - self.height*self.scale/2))

        shadowColor = [self.color[0]*0.6,self.color[1]*0.6,self.color[2]*0.6] # generates a color that is a darker version of the button color

        shadowSurface = self.font.render(self.text, True, shadowColor)
        textSurface = self.font.render(self.text, True, self.textColor)

        shadowRect = shadowSurface.get_rect(center=[self.rect.center[0], self.rect.center[1]+self.fontSize/30]) # offsets the shadow by a factor of the text size so offset scales with text
        textRect = textSurface.get_rect(center=self.rect.center)

        screen.blit(shadowSurface, shadowRect) # draws a shadow of the text to screen
        screen.blit(textSurface, textRect) # draws text to screen