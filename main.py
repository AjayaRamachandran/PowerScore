import numpy as np
from math import *
import inout as io
import api
import matplotlib as mpl
import pygame
import base64

###### OPERATOR FUNCTIONS ######
def getDays(date):
    monthLengths = [31,28,31,30,31,30,31,31,30,31,30,31]
    return int(date[:4]) * 365 + sum(monthLengths[:int(date[5:7]) - 1]) + int(date[8:])

def createPlot(data):
    pygame.init()
    windowSize = [1281, 501]
    screen = pygame.display.set_mode(windowSize)

    ranks = pygame.image.load("ranks.png")
    point = pygame.image.load("point.png")

    screen.fill((10,40,40))
    chartDimensions = [windowSize[0] - 100, windowSize[1] - 100]
    vertTicks, horizTicks = [5, 6]

    leftBound = (windowSize[0] - chartDimensions[0]) / 2
    rightBound = (windowSize[0] + chartDimensions[0]) / 2
    topBound = (windowSize[1] - chartDimensions[1]) / 2
    bottomBound = (windowSize[1] + chartDimensions[1]) / 2

    ranks = pygame.transform.scale(ranks, (chartDimensions[0], chartDimensions[1]))
    ranksRect = ((leftBound, topBound), (ranks.get_rect()[2], ranks.get_rect()[3]))
    screen.blit(ranks, ranksRect)
    #for vertLine in range(vertTicks):
        #pygame.draw.aaline(screen, (20,80,80), (leftBound + vertLine * (chartDimensions[0] / (vertTicks - 1)), bottomBound), (leftBound + vertLine * (chartDimensions[0] / (vertTicks - 1)), topBound))

    for horizLine in range(horizTicks):
        pygame.draw.aaline(screen, (20,80,80), (leftBound, topBound + horizLine * (chartDimensions[1] / (horizTicks - 1))), (rightBound, topBound + horizLine * (chartDimensions[1] / (horizTicks - 1))))

    xValues = [item[0] for item in data]
    yValues = [item[1] for item in data]
    for index in range(len(data) - 1):
        xPos = (xValues[index] - min(xValues)) / (max(xValues) - min(xValues) + 25) * chartDimensions[0] + leftBound
        yPos = (1 - yValues[index] / 100) * (chartDimensions[1]) + topBound
        nextXPos = (xValues[min(index + 1, len(xValues) - 1)] - min(xValues)) / (max(xValues) - min(xValues) + 25) * chartDimensions[0] + leftBound
        nextYPos = (1 - yValues[min(index + 1, len(yValues) - 1)] / 100) * (chartDimensions[1]) + topBound

        #pygame.draw.aaline(screen, (127,160,160), (xPos, yPos), (nextXPos - 3, yPos), 6)
        pygame.draw.aaline(screen, (255,255,255), (xPos, yPos), (nextXPos - 3, yPos), 4)
        #pygame.draw.aaline(screen, (127,160,160), (nextXPos - 3, yPos), (nextXPos, nextYPos), 6)
        pygame.draw.aaline(screen, (255,255,255), (nextXPos - 3, yPos), (nextXPos, nextYPos),4)
    pygame.draw.aaline(screen, (255,255,255), (nextXPos, nextYPos), (rightBound, nextYPos),4)

    screen.blit(point, (rightBound - 8, nextYPos - 8))
    #pygame.draw.circle(screen, (255, 255, 255), (rightBound, yPos), 2)

    pygame.image.save(screen, "plot.png")


###### RANKING ######

def giveRanking(value):
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
        ["Ethereal III", 98],
    ]
    index = 0
    while ranking[index][1] < value:
        index += 1
    index -= 1
    return ranking[index][0]

###### ALGORITHM ######

def runPowerScore(compName, compID, div, typeOfPowerscore):
    output = open("output.txt", "w")

    def generateTeamsListFromComp(fileList): # uses the match list to generate a list of teams that attended a comp, so that a second teamList is unnecessary
        uniqueTeams = []
        for row in fileList:
            teamsInRow = row[:4]
            for team in teamsInRow:
                if not team in uniqueTeams:
                    uniqueTeams.append(team)

        return uniqueTeams

    chart = api.getMatchList(compName, api.getCompInfo(compID, str(div)))
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
            if match.index(player) in [0,1]:
                onRed = True

            if match[4] == "":
                match[4] = 0
            if match[5] == "":
                match[5] = 0
                
            if onRed:
                scoreDiff = int(match[4]) - int(match[5])
            else:
                scoreDiff = int(match[5]) - int(match[4])
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
            if match.index(player) in [0,1]:
                alliancePartner = match[(match.index(player) == 0) + 0]
            elif match.index(player) in [2,3]:
                alliancePartner = match[(match.index(player) == 2) + 2]
            listOfAllianceAvgDiffs.append(getAverageDiff(alliancePartner))

        return listOfAllianceAvgDiffs

    def getOpponentAverageDiffs(player): # gets a list of the average score differentials amongst all the alliance partners a team has had. used to compare against the player's own score diffs
        matchList = retrieve(player=player)
        listOfOpponentAvgDiffs = []

        for match in matchList: # retrieves the index within the row of the two opponent teams, given a team
            if match.index(player) in [0,1]:
                opponent1 = match[2]
                opponent2 = match[3]
            elif match.index(player) in [2,3]:
                opponent1 = match[0]
                opponent2 = match[1]
            avgDiff1 = getAverageDiff(opponent1)
            avgDiff2 = getAverageDiff(opponent2)
            
            listOfOpponentAvgDiffs.append((avgDiff1 + avgDiff2) / 2) # averages the opponent match diffs

        return listOfOpponentAvgDiffs

    def getPowerScore(player, typeOfPowerscore): # master function, combines all the above functions to generate a powerScore value that reflects how "powerful" a team was in the competition
        matchDiffs = getListOfDiffs(player=player) # factor 1 (positive)
        allianceDiffs = getAllianceAverageDiffs(player=player) # factor 2 (negative)
        opponentDiffs = getOpponentAverageDiffs(player=player) # factor 3 (positive)
        matchPowers = []

        for index, matchDiff in enumerate(matchDiffs):
            if typeOfPowerscore == "offensive":
                matchPower = matchDiff + opponentDiffs[index] # performs summation of 3 factors
            if typeOfPowerscore == "defensive":
                matchPower = matchDiff - allianceDiffs[index] # performs summation of 3 factors
            if typeOfPowerscore == "general":
                matchPower = matchDiff - allianceDiffs[index] + opponentDiffs[index] # performs summation of 3 factors
            matchPowers.append(matchPower)
        
        powerScore = np.average(matchPowers)# / 2 + 0.5
        return round(powerScore * 1000) / 1000 # change to 10 outside the parentheses if need to revert
            
    ###### MAIN ######
    #print(teamList)
    for team in teamList: # changes each item in the team list to be a tuple of the team name and its powerScore as opposed to just the team name
        teamList[teamList.index(team)] = [team, getPowerScore(team, typeOfPowerscore)]

    #output.write(compName + " PowerScore\n")
    
    teamList.sort(key=lambda x: x[1], reverse=True) # sorts the list based on powerScore from largest to smallest
    teamLibrary = {}
    for team in teamList:
        if team[0][0] != "#":
            #output.write(f"{team[0]} \t {str(team[1])} \n") # writes output to a .txt file
            teamLibrary[team[0]] = team[1]
    #print(teamLibrary)
    return teamLibrary, teamList
    #print("Output has been saved to output.txt")
    #io.showOutput("output.txt")

def findDivision(name, comp):
    numDivs = len(comp["divisions"])
    for div in range(1, numDivs):
        endpoint = "events/" + str(comp["id"]) + f"/divisions/{div}/rankings"
        params = {"per_page": "250"}
        data = api.makeRequest(endpoint=endpoint, params=params)["data"]
        print("Checking division " + data[0]["division"]["name"] + " at the " + data[0]["event"]["name"])
        roster = []
        for team in data:
            roster.append(team["team"]["name"])
        if name in roster:
            return div
    return 1


#runPowerScore()
def runAlgorithm(team):
    #team = str(input("Enter a Team Number: "))
    comps = api.getCompList(team)
    #print(comps["meta"])
    psList = []
    opsList = []
    dpsList = []
    #print(comps["data"])
    for comp in range(comps["meta"]["total"]):
        #print(comps["data"][comp]["name"])
        #print(compPS)

        if len(comps["data"][comp]["divisions"]) == 1:
            div = "1"
        else:
            #print("Competition has more than one division. Please fix this issue ASAP")
            div = findDivision(team, comps["data"][comp])
        try:
            fullPSLib, fullPSList = runPowerScore(comps["data"][comp]["name"], comps["data"][comp]["id"], div, typeOfPowerscore="general")
            fullOPSLib, fullOPSList = runPowerScore(comps["data"][comp]["name"], comps["data"][comp]["id"], div, typeOfPowerscore="offensive")
            fullDPSLib, fullDPSList = runPowerScore(comps["data"][comp]["name"], comps["data"][comp]["id"], div, typeOfPowerscore="defensive")
            #print(fullPS)
            compPS = fullPSLib[team]
            compOPS = fullOPSLib[team]
            compDPS = fullDPSLib[team]
            #compSum = sum(ps[1] for ps in fullPSList)
            #compWeight = log(0.51 * (compSum ** 0.225)) ** 2
            compWeight = 1.0 + 1 * ("Signature Event" in comps["data"][comp]["name"])
            psList.append([compPS, compWeight, getDays(comps["data"][comp]["start"][:10])])
            opsList.append([compOPS, compWeight, getDays(comps["data"][comp]["start"][:10])])
            dpsList.append([compDPS, compWeight, getDays(comps["data"][comp]["start"][:10])])
            #print([compPS, compSum, log(0.51 * (compSum ** 0.225)) ** 2])
        except:
            print("This team deregistered from a comp")

    #matchPower = (2/(1 + exp(-0.05 * (matchDiff - allianceDiffs[index] + opponentDiffs[index])))) - 1 # performs sigmoid calculation based on the 3 factors
    
    ### GENERAL POWERSCORE ###
    summation = 0
    index = 1
    progression = []
    oldTemporalPS = 0
    temporalPS = 0
    for x in psList:
        summation += x[0] * x[1]
        oldTemporalPS = temporalPS
        temporalPS = summation / index
        progression.append([x[2], round((((2/(1 + exp(-0.045 * (temporalPS)))) - 1) / 2 + 0.5) * 1000) / 10])
        index += 1
    createPlot(progression)
    careerPS = round((((2/(1 + exp(-0.045 * temporalPS))) - 1) / 2 + 0.5) * 100)
    oldCareerPS = round((((2/(1 + exp(-0.045 * oldTemporalPS))) - 1) / 2 + 0.5) * 100)

    ### OFFENSIVE POWERSCORE ###
    summation = 0
    index = 1
    progression = []
    temporalOPS = 0
    for x in opsList:
        summation += x[0] * x[1]
        temporalOPS = summation / index
        progression.append([x[2], round((((2/(1 + exp(-0.045 * (temporalOPS)))) - 1) / 2 + 0.5) * 1000) / 10])
        index += 1
    careerOPS = round((((2/(1 + exp(-0.045 * temporalOPS))) - 1) / 2 + 0.5) * 100)

    ### DEFENSIVE POWERSCORE ###
    summation = 0
    index = 1
    progression = []
    temporalDPS = 0
    for x in dpsList:
        summation += x[0] * x[1]
        temporalDPS = summation / index
        progression.append([x[2], round((((2/(1 + exp(-0.045 * (temporalDPS)))) - 1) / 2 + 0.5) * 1000) / 10])
        index += 1
    careerDPS = round((((2/(1 + exp(-0.045 * temporalDPS))) - 1) / 2 + 0.5) * 100)

    if careerOPS - careerDPS > 20:
        title = "Sentinel"
    elif careerOPS - careerDPS < -20:
        title = "Aggressor"
    else:
        title = "Neutral"

    accolade1 = ["Top Fragger", "Attain the Highest Powerscore at a competition"]
    accolade2 = ["Started From the Bottom", "Climb from below Gold to above Platinum in a season"]

    rank = giveRanking(careerPS)
    rankCopy = rank.replace(" ", "")
    badgeFileDir = "newbadges/" + rankCopy + ".png"
    # Read the image file
    image_data = open(badgeFileDir, 'rb').read()
    # Encode as base64
    data_uri = base64.b64encode(image_data).decode('utf-8')
    # Create an <img> tag with the base64-encoded image
    badge_tag = data_uri

    return [team, careerPS, oldCareerPS, rank, careerOPS, careerDPS, title, accolade1, accolade2, badge_tag]

    #print(comps["data"][comp]["id"])