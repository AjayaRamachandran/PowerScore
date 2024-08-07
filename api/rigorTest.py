###### IMPORT ######

from math import *
import time

import apiHandler
import asyncApi

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

###### ALGORITHM ######

def runPowerScore(compName, compID, div, typeOfPowerscore, compInfo, onlyForComp=False):
    #output = open("output.txt", "w")

    def generateTeamsListFromComp(fileList): # uses the match list to generate a list of teams that attended a comp, so that a second teamList is unnecessary
        uniqueTeams = []
        for row in fileList:
            teamsInRow = row[:4]
            for team in teamsInRow:
                if not team in uniqueTeams:
                    uniqueTeams.append(team)

        return uniqueTeams

    chart = apiHandler.getMatchList(compName, compInfo)
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
        avgDiff = sum(scoreDiffs) / len(scoreDiffs)
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
            powerScore = (sum(matchPowers) / len(matchPowers)) / 2 + 0.5
            return round(powerScore * 1000) / 10 # change to 10 outside the parentheses if need to revert
        else:
            powerScore = (sum(matchPowers) / len(matchPowers))# / 2 + 0.5
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


def runAlgorithm(team, season, excludes):
    global accolades, teamname

    apiHandler.setDefaultSeason(season)
    accolades = []
    teamname = team

    comps = apiHandler.getCompList(team)

    psList = []
    opsList = []
    dpsList = []

    dashboard = []
    compiledList = asyncApi.getCompiledDataList(team, comps, season)
    comps = comps['data']
    startDate = comps[0]["start"][:10]

    #print(compiledList[0][0])
    for comp in range(len(compiledList)):
        if not compiledList[comp][0]['event']['code'] in excludes:
            division = compiledList[comp]

            date = "Error Fetching Date"
            sku = "Error Fetching SKU"
            for competition in range(len(comps)):
                if comps[competition]["sku"] == compiledList[comp][0]['event']['code']:
                    date = comps[competition]["start"][:10]

            # the new powerscore algorithm works for offensive and defensive powerscore. thus the alg is split in three pieces. overall ps is the most important still.
            fullPSLib, fullPSList = runPowerScore(None, None, div=None, typeOfPowerscore="general", compInfo=division)
            newPSLib, newPSList = runPowerScore(None, None, div=None, typeOfPowerscore="general", compInfo=division, onlyForComp=True)
        
            compPS = fullPSLib[team]
            newPS = newPSLib[team]

            compWeight = 1.0 + 1 * ("Signature Event" in compiledList[comp][0]['event']['name'])
            psList.append([compPS, compWeight, date])

            thisComp = {}
            thisComp['name'] = compiledList[comp][0]['event']['name']
            print(thisComp['name'])
            thisComp['date'] = date
            thisComp['sku'] = compiledList[comp][0]['event']['code']
            thisComp['score'] = round(newPS)

            dashboard.append(thisComp)
    
    ### GENERAL POWERSCORE ###
    summation = 0
    index = 1
    progression = []

    for x in psList:
        summation += x[0] * x[1]
        temporalPS = summation / index
        progression.append([x[2], round((((2/(1 + exp(-0.045 * (temporalPS)))) - 1) / 2 + 0.5) * 1000) / 10])
        index += 1

    careerPS = round((((2/(1 + exp(-0.045 * temporalPS))) - 1) / 2 + 0.5) * 10000) / 100

    return careerPS

def getDivisionTeams(compID, div=1): # function to search through a competition and find the division a team was in
    #numDivs = len(comp["divisions"])
    #for div in range(1, numDivs):
        endpoint = "events/" + compID + f"/divisions/{div}/rankings"
        params = {"per_page": "250"}
        data = apiHandler.makeRequest(endpoint=endpoint, params=params)["data"]
        print("Checking division " + data[0]["division"]["name"] + " at the " + data[0]["event"]["name"])
        roster = []
        for team in data:
            roster.append(team["team"]["name"])
        return roster
        #if name in roster:
            #return div
    #return 1 # catch case

def getData(div):
    listOfTeams = getDivisionTeams("53690", str(div))
    #print(listOfTeams)
    listOfPS = []
    for team in listOfTeams:
        try:
            ps = runAlgorithm(team, "181", excludes = ['RE-VRC-23-3690'])
            listOfPS.append([team, ps])
            for pair in listOfPS:
                print(pair)
            time.sleep(120)
        except:
            None
    print(listOfPS)
#getData(3)

def openPowerScoreFile(filename):
    file = open(filename, 'r')
    psList = []
    for line in file:
        lineContent = line.strip()
        lineContent = lineContent.replace(',', '')
        lineContent = lineContent.replace('[', '')
        lineContent = lineContent.replace(']', '')
        lineContent = lineContent.replace("'", '')
        breakPoint = lineContent.index(" ")
        team = lineContent[:breakPoint]
        ps = lineContent[breakPoint+1:]
        psList.append([team, ps])
    return psList
#openPowerScoreFile("api/artsDiv.txt")

def getPS(team, psList):
    for pair in psList:
        if pair[0] == team:
            return pair[1]
    raise "Error"
    #index = next(i for i, (x, y) in enumerate(psList) if x == team)
    #return psList[index][1]



def getDivAccuracy(compID, div):
    endpoint = "events/" + compID + f"/divisions/{div}/matches"
    params = {"per_page": "250"}
    data = apiHandler.makeRequest(endpoint=endpoint, params=params)["data"]
    matchList = apiHandler.getMatchList("Worlds", data)
    psList = openPowerScoreFile('api/divisionPS/innovateDiv.txt')

    successes = []
    for match in matchList:
        print(match)
        try:
            redSum = getPS(match[0], psList) + getPS(match[1], psList)
            blueSum = getPS(match[2], psList) + getPS(match[3], psList)

            predictedRedWin = redSum > blueSum
            actualRedWin = match[4] > match[5]

            if predictedRedWin == actualRedWin:
                successes.append(True)
            else:
                successes.append(False)
        except:
            None
        
    numSuccesses = 0
    for match in successes:
        if match:
            numSuccesses += 1
    
    percentageSuccesses = numSuccesses / len(successes)
    print(f"PowerScore was {percentageSuccesses * 100}% accurate for the Innovate Division.")

getDivAccuracy('53690', '3')



#print(runAlgorithm("8568A", "181", excludes = ['RE-VRC-23-3690']))