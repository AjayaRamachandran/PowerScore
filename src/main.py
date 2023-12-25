import time
import numpy as np
from math import *
import xlrd
import inout as io
import pygame

# https://xlrd.readthedocs.io/en/latest/

### Requirements ###
# pip install xlrd

###### INITIALIZE ######

pygame.init()

windowSize = (600, 400)

fps = 60
clock = pygame.time.Clock()

bgPhoto = "powerscorebg.png"
bg = pygame.image.load(bgPhoto)
bg_rect = bg.get_rect()

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

pygame.display.set_caption("PowerScore") # Sets title of window
screen = pygame.display.set_mode(windowSize) # Sets the dimensions of the window to the windowSize
importing = False
running = True # Runs the game loop

###### MAINLOOP ######

while running:
    screen.fill((30, 30, 37))

    for event in pygame.event.get(): # checks if program is quit, if so stops the code
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            running = False
            importing = True
    # runs framerate wait time
    clock.tick(fps)
    # update the screen
    screen.blit(bg, bg_rect)
    
    pygame.display.update()

# quit Pygame
pygame.quit()

###### ALGORITHM ######

if importing == True:
    inputFile = io.importFile()

    output = open("output.txt", "w")
    #nameOfEvent = input("Event name? ")
    #compxls = xlrd.open_workbook(filename = f"events/{nameOfEvent}.xls")
    compxls = xlrd.open_workbook(filename = inputFile)
    comp = compxls.sheet_by_index(0)

    # Imports the .xls file (given by RobotEvents) and converts it to a list, from which it can pull values.
    def listifySheet(file):
        fileList = []

        column = 1
        row = 0
        for row in range(1, file.nrows):
            if "Qualifier" in file.cell_value(row, 1) and not file.cell_value(row, 6) == "":
                slicedRow = [
                    file.cell_value(row, 1),
                    file.cell_value(row, 2),
                    file.cell_value(row, 3),
                    file.cell_value(row, 4),
                    file.cell_value(row, 5),
                    file.cell_value(row, 6),
                    file.cell_value(row, 7),
                    file.cell_value(row, 8)
                    ]
                fileList.append(slicedRow)

        return fileList

    def generateTeamsListFromComp(fileList): # uses the match list to generate a list of teams that attended a comp, so that a second teamList is unnecessary
        uniqueTeams = []
        for row in fileList:
            teamsInRow = row[1:5]
            for team in teamsInRow:
                if not team in uniqueTeams:
                    uniqueTeams.append(team)

        return uniqueTeams

    # Imports the .txt file and converts it to a list, from which it can pull values.
    def listifyText(file):
        fileList = []
        for line in file:
            individualWord = line.strip()
            fileList.append(individualWord)
        return fileList

    chart = listifySheet(comp)
    teamList = generateTeamsListFromComp(chart)

    ###### FUNCTIONS ######
    def retrieve(round=None, player=None): # retrieves a player's matches from the dataset, or optionally the data of a specific match (although the powerscore algorithm never uses this 2nd option)
        if round != None:
            specifiedValue = "N/A"
            for row in chart:
                if row[0] == round:
                    specifiedValue = row
            return specifiedValue
        elif player != None:
            foundMatches = []
            for row in chart:
                if player in row:
                    foundMatches.append(row)
            return foundMatches

    def getListOfDiffs(player): # returns a list of all the score differentials in matches that a specific player had (score differential is the difference in score between alliance and opponent)
        matchList = retrieve(player=player)

        scoreDiffs = []
        for match in matchList:
            onRed = False
            if match.index(player) in [1,2]:
                onRed = True
            if onRed:
                scoreDiff = int(match[5]) - int(match[6])
            else:
                scoreDiff = int(match[6]) - int(match[5])
            scoreDiffs.append(scoreDiff)
        
        return scoreDiffs
        
    def getAverageDiff(player): # returns the average value of a list of score differentials. this is separated from the above function because we sometimes want the list, other times want the avg
        scoreDiffs = getListOfDiffs(player=player)
        avgDiff = np.average(scoreDiffs)
        return round(avgDiff*1000)/1000

    def getAllianceAverageDiffs(player): # gets a list of the average score differentials amongst all the alliance partners a team has had. used to compare against the player's own score diffs
        matchList = retrieve(player=player)
        listOfAllianceAvgDiffs = []

        for match in matchList: # retrieves the index within the row of the alliance partner, given a team
            if match.index(player) in [1,2]:
                alliancePartner = match[(match.index(player) == 1) + 1]
            elif match.index(player) in [3,4]:
                alliancePartner = match[(match.index(player) == 3) + 3]
            listOfAllianceAvgDiffs.append(getAverageDiff(alliancePartner))

        return listOfAllianceAvgDiffs

    def getOpponentAverageDiffs(player): # gets a list of the average score differentials amongst all the alliance partners a team has had. used to compare against the player's own score diffs
        matchList = retrieve(player=player)
        listOfOpponentAvgDiffs = []

        for match in matchList: # retrieves the index within the row of the two opponent teams, given a team
            if match.index(player) in [1,2]:
                opponent1 = match[3]
                opponent2 = match[4]
            elif match.index(player) in [3,4]:
                opponent1 = match[1]
                opponent2 = match[2]
            avgDiff1 = getAverageDiff(opponent1)
            avgDiff2 = getAverageDiff(opponent2)
            
            listOfOpponentAvgDiffs.append((avgDiff1 + avgDiff2) / 2) # averages the opponent match diffs

        return listOfOpponentAvgDiffs

    def getPowerScore(player): # master function, combines all the above functions to generate a powerScore value that reflects how "powerful" a team was in the competition
        matchDiffs = getListOfDiffs(player=player) # factor 1 (positive)
        allianceDiffs = getAllianceAverageDiffs(player=player) # factor 2 (negative)
        opponentDiffs = getOpponentAverageDiffs(player=player) # factor 3 (positive)
        matchPowers = []

        for index, matchDiff in enumerate(matchDiffs):
            matchPower = (2/(1 + exp(-0.05 * (matchDiff - allianceDiffs[index] + opponentDiffs[index])))) - 1 # performs sigmoid calculation based on the 3 factors
            matchPowers.append(matchPower)
        
        powerScore = np.average(matchPowers) / 2 + 0.5
        return round(powerScore * 1000) / 10
            
    ###### MAIN ######

    for team in teamList: # changes each item in the team list to be a tuple of the team name and its powerScore as opposed to just the team name
        teamList[teamList.index(team)] = [team, getPowerScore(team)]

    letter = len(inputFile) - 1
    while inputFile[letter] != "/":
        letter -= 1
    plainFileName = inputFile[(letter + 1):(len(inputFile) - 4)]
    output.write(plainFileName + " PowerScore\n")
    teamList.sort(key=lambda x: x[1], reverse=True) # sorts the list based on powerScore from largest to smallest
    for team in teamList:
        if team[0][0] != "#":
            output.write(f"{team[0]} \t {str(team[1])} \n") # writes output to a .txt file

    #print("Output has been saved to output.txt")
    io.showOutput("output.txt")