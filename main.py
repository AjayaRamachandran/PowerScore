import numpy as np
from math import *
import inout as io
import api
#import matplotlib as mpl
import pygame
import base64
from PIL import Image

###### OPERATOR FUNCTIONS ######
def getDays(date):
    monthLengths = [31,28,31,30,31,30,31,31,30,31,30,31]
    return int(date[:4]) * 365 + sum(monthLengths[:int(date[5:7]) - 1]) + int(date[8:])

def createPlot(data, teamname):
    pygame.init()
    windowSize = [630, 250]
    screen = pygame.display.set_mode(windowSize)

    ranks = pygame.image.load("ranks.png")
    point = pygame.image.load("point.png")

    font = pygame.font.Font("Teko-Regular.ttf", 22)

    screen.fill((14, 97, 114))
    topMargin = 25
    bottomMargin = 50
    chartDimensions = [windowSize[0] - 50, windowSize[1] - (topMargin + bottomMargin)]
    vertTicks, horizTicks = [5, 6]

    leftBound = (windowSize[0] - chartDimensions[0]) / 2
    rightBound = (windowSize[0] + chartDimensions[0]) / 2
    topBound = topMargin
    bottomBound = windowSize[1] - bottomMargin

    ranks = pygame.transform.scale(ranks, (chartDimensions[0], chartDimensions[1]))
    ranksRect = ((leftBound, topBound), (ranks.get_rect()[2], ranks.get_rect()[3]))
    screen.blit(ranks, ranksRect)
    #for vertLine in range(vertTicks):
        #pygame.draw.aaline(screen, (20,80,80), (leftBound + vertLine * (chartDimensions[0] / (vertTicks - 1)), bottomBound), (leftBound + vertLine * (chartDimensions[0] / (vertTicks - 1)), topBound))

    for horizLine in range(horizTicks):
        pygame.draw.aaline(screen, (44, 127, 144), (leftBound, topBound + horizLine * (chartDimensions[1] / (horizTicks - 1))), (rightBound, topBound + horizLine * (chartDimensions[1] / (horizTicks - 1))))

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
    bottomText = font.render(f"{teamname} Powerscore Over Time", True, (255,255,255))
    bottomRect = [windowSize[0]/2 - bottomText.get_rect()[2]/2, windowSize[1] - 40, bottomText.get_rect()[2], bottomText.get_rect()[3]]
    screen.blit(bottomText, bottomRect)
    #pygame.draw.circle(screen, (255, 255, 255), (rightBound, yPos), 2)

    pygame.image.save(screen, "plot.png")


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
    ["Ethereal III", 98],
]

def giveRanking(value):

    index = 0
    while ranking[index][1] < value:
        index += 1
    index -= 1
    return ranking[index][0]

###### ALGORITHM ######

def runPowerScore(compName, compID, div, typeOfPowerscore, compInfo, onlyForComp=False):
    output = open("output.txt", "w")

    def generateTeamsListFromComp(fileList): # uses the match list to generate a list of teams that attended a comp, so that a second teamList is unnecessary
        uniqueTeams = []
        for row in fileList:
            teamsInRow = row[:4]
            for team in teamsInRow:
                if not team in uniqueTeams:
                    uniqueTeams.append(team)

        return uniqueTeams

    chart = api.getMatchList(compName, compInfo)
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
                if onlyForComp:
                    matchPower = (2/(1 + exp(-0.05 * (matchDiff + opponentDiffs[index])))) - 1 # performs sigmoid calculation based on the 2 factors
                else:
                    matchPower = matchDiff + opponentDiffs[index] # performs summation of 2 factors
            if typeOfPowerscore == "defensive":
                if onlyForComp:
                    matchPower = (2/(1 + exp(-0.05 * (matchDiff - allianceDiffs[index])))) - 1 # performs sigmoid calculation based on the 2 factors
                else:
                    matchPower = matchDiff - allianceDiffs[index] # performs summation of 2 factors
            if typeOfPowerscore == "general":
                if onlyForComp:
                    matchPower = (2/(1 + exp(-0.05 * (matchDiff - allianceDiffs[index] + opponentDiffs[index])))) - 1 # performs sigmoid calculation based on the 3 factors
                else:
                    matchPower = matchDiff - allianceDiffs[index] + opponentDiffs[index] # performs summation of 3 factors
            matchPowers.append(matchPower)
        
        if onlyForComp:
            powerScore = np.average(matchPowers) / 2 + 0.5
            return round(powerScore * 1000) / 10 # change to 10 outside the parentheses if need to revert
        else:
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

def runComp(sku):
    name, compInfos = api.getCompInfoBySKU(sku)
    for i in range(len(compInfos) -1):
        fullPSLib, fullPSList = runPowerScore(None, None, div=None, typeOfPowerscore="general", compInfo=compInfos[i], onlyForComp=True)
        fullOPSLib, fullOPSList = runPowerScore(None, None, div=None, typeOfPowerscore="offensive", compInfo=compInfos[i], onlyForComp=True)
        fullDPSLib, fullDPSList = runPowerScore(None, None, div=None, typeOfPowerscore="defensive", compInfo=compInfos[i], onlyForComp=True)
    
    newOPSList = []
    for team in fullPSList:
        newOPSList.append([team[0], fullOPSLib[team[0]]])
    newDPSList = []
    for team in fullPSList:
        newDPSList.append([team[0], fullDPSLib[team[0]]])
    #print(fullPSList)
    #print(newOPSList)
    #print(newDPSList)
    return [name, fullPSList, newOPSList, newDPSList]

#runComp("RE-VRC-23-2380")
#runComp('RE-VRC-23-2382')
#runComp('RE-VRC-23-4706')

#runPowerScore()
def runAlgorithm(team):
    global accolades, teamname
    accolades = []
    teamname = team

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
            compInfo = api.getCompInfo(comps["data"][comp]["id"], str(div))
            fullPSLib, fullPSList = runPowerScore(comps["data"][comp]["name"], comps["data"][comp]["id"], div, typeOfPowerscore="general", compInfo=compInfo)
            fullOPSLib, fullOPSList = runPowerScore(comps["data"][comp]["name"], comps["data"][comp]["id"], div, typeOfPowerscore="offensive", compInfo=compInfo)
            fullDPSLib, fullDPSList = runPowerScore(comps["data"][comp]["name"], comps["data"][comp]["id"], div, typeOfPowerscore="defensive", compInfo=compInfo)
            #print(fullPS)
            compPS = fullPSLib[team]
            compOPS = fullOPSLib[team]
            compDPS = fullDPSLib[team]
            #print(compPS)
            if round((((2/(1 + exp(-0.045 * (compPS)))) - 1) / 2 + 0.5) * 1000) / 10 >= 90 and not "First Class" in accolades:
                accolades.append("First Class")
            if round((((2/(1 + exp(-0.045 * (compPS)))) - 1) / 2 + 0.5) * 1000) / 10 >= 90 and ("Signature Event" in comps["data"][comp]["name"]) and not "World Class" in accolades:
                accolades.append("World Class")
            if fullPSList.index([team, compPS]) == 0 and not "Top Fragger" in accolades:
                accolades.append("Top Fragger")
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
    createPlot(progression, teamname)
    if progression[0][1] < 51 and progression[len(progression) - 1][1] > 70:
        accolades.append("Glow Up")
    sortedProgression = sorted(progression, key=lambda x: x[1], reverse=True) # sorts the list based on powerScore from largest to smallest
    if sortedProgression[0][1] > 80 and progression[len(progression) - 1][1] < 71:
        accolades.append("Fall from Grace")
    careerPS = round((((2/(1 + exp(-0.045 * temporalPS))) - 1) / 2 + 0.5) * 10000) / 100
    #print(careerPS)
    oldCareerPS = round((((2/(1 + exp(-0.045 * oldTemporalPS))) - 1) / 2 + 0.5) * 100)

    nextRank = 0
    prevRank = 0
    for rank in reversed(ranking):
        if careerPS < rank[1]:
            nextRank = rank[1]
    for rank in ranking:
        if careerPS > rank[1]:
            prevRank = rank[1]
    
    xpToNext = round(((nextRank - careerPS) * careerPS) * 0.05) * 100

    percentageXP = round(((careerPS - prevRank) / (nextRank - prevRank)) * 100) / 100

    image = Image.new("RGBA", (100, 10))
    for y in range(10):
        for x in range(100):
            if x / 100 < percentageXP:
                image.putpixel((x, y), (132, 238, 255, 255))
            else:
                image.putpixel((x, y), (27, 119, 138, 255))
    image.save("bar.png")
    rank = giveRanking(careerPS)
    careerPS = round(careerPS)

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

    if careerOPS - careerDPS > 5:
        title = "Aggressor"
    elif careerOPS - careerDPS < -5:
        title = "Sentinel"
    else:
        title = "Neutral"

    #if "World Class" in accolades:
        #accolades.remove("First Class")
    possibleAccolades = [
        ["World Class", "Attain a Powerscore above 90 at a Signature Event"],
        ["Glow Up", "Climb from below Gold to above Gold in a season"],
        ["Top Fragger", "Attain the highest Powerscore at a competition"],
        ["First Class", "Attain a Powerscore above 90 at a competition"],
        ["Fall from Grace", "Fall from above Diamond to below Diamond in a season"]
    ]
    num = 0
    accolade1 = ["No Accolade", "Earn accolades by playing in tournaments!"]
    accolade2 = ["No Accolade", "Earn accolades by playing in tournaments!"]
    for accolade in possibleAccolades:
        if accolade[0] in accolades:
            if num == 0:
                accolade1 = accolade
            if num == 1:
                accolade2 = accolade
            num += 1

    rankCopy = rank.replace(" ", "")
    badgeFileDir = "newbadges/" + rankCopy + ".png"
    # Read the image file
    image_data = open(badgeFileDir, 'rb').read()
    # Encode as base64
    data_uri = base64.b64encode(image_data).decode('utf-8')
    # Create an <img> tag with the base64-encoded image
    badge_tag = data_uri

    image_data = open("plot.png", 'rb').read()
    # Encode as base64
    data_uri = base64.b64encode(image_data).decode('utf-8')
    # Create an <img> tag with the base64-encoded image
    graph_tag = data_uri

    image_data = open("bar.png", 'rb').read()
    # Encode as base64
    data_uri = base64.b64encode(image_data).decode('utf-8')
    # Create an <img> tag with the base64-encoded image
    bar_tag = data_uri

    return [team, careerPS, oldCareerPS, rank, careerOPS, careerDPS, title, accolade1, accolade2, badge_tag, graph_tag, xpToNext, bar_tag]

    #print(comps["data"][comp]["id"])