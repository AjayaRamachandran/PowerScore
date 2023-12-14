import time
import numpy as np
from math import *
import xlrd

# https://openpyxl.readthedocs.io/en/stable/tutorial.html

### Requirements ###
# pip install xlrd

###### INITIALIZE ######

#matches = open("src/matches2.txt") # Imports the .txt file
#teams = open("src/teams2.txt") # Imports the .txt file
compxls = xlrd.open_workbook(filename = "src/comp2.xls")
comp = compxls.sheet_by_index(0)

# Imports the .xls file and converts it to a list, from which it can pull values.
def listifySheet(file):
    fileList = []

    column = 1
    row = 0
    for row in range(1, file.nrows):
        if "Qualifier" in file.cell_value(row, 1):
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

def generateTeamsListFromComp(fileList):
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

#wordList = listifyText(matches)
chart = listifySheet(comp)
#for x in range(len(chart)):
    #print(chart[x])
teamList = generateTeamsListFromComp(chart)
#for x in range(len(teamList)):
    #print(teamList[x])

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

    for match in matchList:
        if match.index(player) in [1,2]:
            alliancePartner = match[(match.index(player) == 1) + 1]
        elif match.index(player) in [3,4]:
            alliancePartner = match[(match.index(player) == 3) + 3]
        listOfAllianceAvgDiffs.append(getAverageDiff(alliancePartner))

    return listOfAllianceAvgDiffs

def getOpponentAverageDiffs(player): # gets a list of the average score differentials amongst all the alliance partners a team has had. used to compare against the player's own score diffs
    matchList = retrieve(player=player)
    listOfOpponentAvgDiffs = []

    for match in matchList:
        if match.index(player) in [1,2]:
            opponent1 = match[3]
            opponent2 = match[4]
        elif match.index(player) in [3,4]:
            opponent1 = match[1]
            opponent2 = match[2]
        avgDiff1 = getAverageDiff(opponent1)
        avgDiff2 = getAverageDiff(opponent2)
        
        listOfOpponentAvgDiffs.append((avgDiff1 + avgDiff2) / 2)

    return listOfOpponentAvgDiffs

def getPowerScore(player): # master function, combines all the above functions to generate a powerScore value that reflects how "powerful" a team was in the competition
    matchDiffs = getListOfDiffs(player=player)
    allianceDiffs = getAllianceAverageDiffs(player=player)
    opponentDiffs = getOpponentAverageDiffs(player=player)
    matchPowers = []

    for index, matchDiff in enumerate(matchDiffs):
        matchPower = (2/(1 + exp(-0.05 * (matchDiff - allianceDiffs[index] + opponentDiffs[index])))) - 1
        matchPowers.append(matchPower)
    
    powerScore = np.average(matchPowers) / 2 + 0.5
    return round(powerScore * 1000) / 10
        
###### MAIN ######

for team in teamList:
    if team[0] == "#":
        teamList.remove(team)

for team in teamList:
    teamList[teamList.index(team)] = [team, getPowerScore(team)]

print(teamList)

teamList.sort(key=lambda x: x[1], reverse=True)
for team in teamList:
    if team[0][0] != "#":
        #print(team[0] + "'s PowerScore was " + str(team[1]))
        print(team[0])

for team in teamList:
    if team[0][0] != "#":
        print(str(team[1]))