###### IMPORT ######

from PIL import Image
import io
import pygame
import os

import random
from math import *
import time

from tkinter.filedialog import asksaveasfile

###### SETUP ######

pygame.init()
screenInfo = pygame.display.Info()
screenWidth = screenInfo.current_w
screenHeight = screenInfo.current_h

hdRatio = screenWidth / 1920

###### FUNCTIONS ######

def spawnBorderedElement(width, height, color, x, y, scale, type, cr): # runs function to generate a button image based on some basic rules
    cornerRadius = cr
    array = []
    for w in range(width):
        row = []
        for h in range(height):
            if len(color) == 4:
                opacity = color[3]
            else:
                opacity = 255

            if type == 0 or type == 1:
                dimFactor = 1 - (type == 1)*0.2

                AAEdge = 5

                outerRadius = (cornerRadius)**2 + AAEdge
                innerRadius = (cornerRadius)**2 - AAEdge

                outOfRadius = False
                antiAliased = False

                if w < cornerRadius and h < cornerRadius: # top left corner
                    outOfRadius = (cornerRadius - w)**2 + (cornerRadius - h)**2 > outerRadius
                    antiAliased = innerRadius < (cornerRadius - w)**2 + (cornerRadius - h)**2 < outerRadius
                elif w > width - cornerRadius - 1 and h < cornerRadius: # top right corner
                    outOfRadius = (width - w - cornerRadius - 1)**2 + (cornerRadius - h)**2 > outerRadius
                    antiAliased = innerRadius < (width - w - cornerRadius - 1)**2 + (cornerRadius - h)**2 < outerRadius
                elif w < cornerRadius and h > height - cornerRadius - 1: # bottom left corner
                    outOfRadius = (cornerRadius - w)**2 + (height - h - cornerRadius - 1)**2 > outerRadius
                    antiAliased = innerRadius < (cornerRadius - w)**2 + (height - h - cornerRadius - 1)**2 < outerRadius
                elif w > width - cornerRadius - 1 and h > height - cornerRadius - 1: # bottom right corner
                    outOfRadius = (width - w - cornerRadius - 1)**2 + (height - h - cornerRadius - 1)**2 > outerRadius
                    antiAliased = innerRadius < (width - w - cornerRadius - 1)**2 + (height - h - cornerRadius - 1)**2 < outerRadius

                if outOfRadius:
                    row.append([0,0,0,0])
                elif antiAliased:
                    row.append([int(color[0]*dimFactor),int(color[1]*dimFactor),int(color[2]*dimFactor),round(opacity/2)])
                else:
                    row.append([int(color[0]*dimFactor),int(color[1]*dimFactor),int(color[2]*dimFactor),opacity])

        array.append(row)
    return array

def initializeBorderedElement(width, height, color, x, y, scale, names, cr):
    for type in names: # generates images of all the different states the button could be in
        if not os.path.exists(type[0]):
            image = Image.new("RGBA", (width, height))
            for x, row in enumerate(spawnBorderedElement(width, height, color, x, y, scale, type[1], cr)):
                for y, pixel in enumerate(row):
                    image.putpixel((x, y), tuple(pixel))
            
            image.save(type[0])
        else:
            print(type[0] + " already exists. To regenerate, delete source image and try again.")

        

###### CLASSES ######

class GUI:
    def __init__(self, x, y):
        self.x = x * hdRatio
        self.y = y * hdRatio

    def moveTo(self, x, y):
        self.x = x * hdRatio
        self.y = y * hdRatio

class Title(GUI):
    def __init__(self, type, x, y, text, textColor, fontSize=20):
        super().__init__(x, y)
        #---SELF PROPERTIES---#
        ## Visual Info ##
        self.text = text

        ## Text Attributes ##
        self.textColor = textColor
        self.fontSize = int(fontSize * hdRatio)

        if type == "title":
            self.font = pygame.font.Font("fonts/Inter-ExtraBold.ttf", self.fontSize)
        if type == "body":
            self.font = pygame.font.Font("fonts/Inter-Regular.ttf", self.fontSize)
    
    def setTitle(self, newTitle):
        self.text = newTitle
    
    def draw(self, screen):
        textSurface = self.font.render(self.text, True, self.textColor)
        textRect = textSurface.get_rect(center=(self.x, self.y))

        screen.blit(textSurface, textRect) # draws text to screen

class Window(GUI):
    def __init__(self, name, x, y, width, height, cornerRadius, color, scale):
        super().__init__(x, y)

        #---SELF PROPERTIES---#
        ## Essential/Very Important ##
        self.name = name
        self.rect = pygame.Rect(x-width*scale/2, y-height*scale/2, width*scale, height*scale)

        ## Visual Info (Cosmetic) ##
        self.color = color

        ## Visual Info (Spatial) ##
        self.width = width * hdRatio
        self.height = height * hdRatio
        self.scale = scale
        self.cornerRadius = cornerRadius

        ## File Saving ##
        self.fileNames = [("images/base_" + str(name) + ".png", 0)]

        #---INITIAL FUNCTIONS/SCRIPTS---#
        initializeBorderedElement(width=self.width, height=self.height, color=self.color, x=self.x, y=self.y, scale=self.scale, names=self.fileNames, cr=self.cornerRadius)

    def draw(self, screen):
        window = pygame.image.load(self.fileNames[0][0]) # loads images of all the different states the window could be in
        window = pygame.transform.scale(window, (self.width * self.scale, self.height * self.scale)) # scales the images by a scale factor

        screen.blit(window, (self.x - self.width*self.scale/2, self.y - self.height*self.scale/2))

class Button(GUI):
    def __init__(self, name, x, y, width, height, cornerRadius, color, text, scale, fontSize=20):
        super().__init__(x, y)

        #---SELF PROPERTIES---#
        ## Essential/Very Important ##
        self.name = name
        self.rect = pygame.Rect((x-width*scale/2)*hdRatio, (y-height*scale/2)*hdRatio, width*scale*hdRatio, height*scale*hdRatio)

        ## Visual Info (Cosmetic) ##
        self.color = color
        self.text = text

        ## Visual Info (Spatial) ##
        self.width = width * hdRatio
        self.height = height * hdRatio
        self.scale = scale
        self.cornerRadius = cornerRadius

        ## Text Attributes ##
        self.textColor = (255, 255, 255)  # Default text color
        self.fontSize = int(fontSize * hdRatio)
        self.font = pygame.font.Font("fonts/Inter-Regular.ttf", self.fontSize)

        ## File Saving ##
        self.fileNames = [("images/base_" + str(name) + ".png", 0),
                          ("images/dimmed_" + str(name) + ".png", 1)]

        #---INITIAL FUNCTIONS/SCRIPTS---#
        initializeBorderedElement(width=self.width, height=self.height, color=self.color, x=self.x, y=self.y, scale=self.scale, names=self.fileNames, cr=self.cornerRadius)

    def draw(self, screen, mode=0):
        button = pygame.image.load(self.fileNames[0][0]) # loads images of all the different states the button could be in
        dimmedButton = pygame.image.load(self.fileNames[1][0])


        button = pygame.transform.scale(button, (self.width * self.scale, self.height * self.scale)) # scales the images by a scale factor (for the "pixelated" look)
        dimmedButton = pygame.transform.scale(dimmedButton, (self.width * self.scale, self.height * self.scale))


        if self.rect.collidepoint(pygame.mouse.get_pos()) or mode==1: # blits to screen the dimmed version of the button if the mouse is hovering over it
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

    def isClicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
            return True
        else:
            return False
        
class Textbox(GUI):
    def __init__(self, name, x, y, width, height, exampleText, scale, color=(255, 255, 255),fontSize=20):
        super().__init__(x, y)

        #---SELF PROPERTIES---#
        ## Essential/Very Important ##
        self.name = name
        self.rect = pygame.Rect((x-width*scale/2)*hdRatio, (y-height*scale/2)*hdRatio, width*scale*hdRatio, height*scale*hdRatio)
        self.selected = False

        ## Visual Info (Cosmetic) ##
        self.color = color
        self.exampleText = exampleText
        self.text = ""

        ## Visual Info (Spatial) ##
        self.width = width * hdRatio
        self.height = height * hdRatio
        self.scale = scale

        ## Text Attributes ##
        self.textColor = (0, 0, 0)  # Default text color
        self.fontSize = int(fontSize * hdRatio)
        self.font = pygame.font.Font("fonts/Inter-Regular.ttf", self.fontSize)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, width=0) # draws a (default: white) background for the textbox

        if self.selected:
            pygame.draw.rect(screen, (0, 0, 0), self.rect, width=4) # draws a thick border if the textbox is selected
            
            textSurface = self.font.render(self.text, True, self.textColor) # this weird workaround (rendering without the pole then adding the pole) prevents the up-down jitter seen when using the pole as the cursor
            textRect = textSurface.get_rect(center=self.rect.center)

            if int(time.time()) % 2 == 0:
                textSurface = self.font.render(self.text + "|", True, self.textColor)

        else:
            pygame.draw.rect(screen, (0, 0, 0), self.rect, width=2)  # draws a thin border if the textbox is not selected
            fadedTextColor = [value * 0.8 for value in self.color] # generates a faded text color based on a darker version of the textbox's bg color

            if self.text == "":  # if the textbox is empty and unselected, write a faded default text in it
                textSurface = self.font.render(self.exampleText, True, fadedTextColor)
            else:
                textSurface = self.font.render(self.text, True, self.textColor)

            textRect = textSurface.get_rect(center=self.rect.center)
        screen.blit(textSurface, textRect) # draws text to screen

    def isClicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
            return True
        else:
            return False
        
    def isUnclicked(self):
        if not self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
            return True
        else:
            return False
        
    def dynamicInteraction(self, pressedKey):
        if self.isClicked():
            self.selected = True
            
        if self.isUnclicked():
            self.selected = False

        if self.selected:
            if pressedKey == "keyBKSPC":
                self.text = self.text[:-1]
            else:
                self.text = self.text + pressedKey


