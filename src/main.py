import numpy as np
from math import *
import inout as io
import api

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

def runPowerScore(compName, compID):
    output = open("output.txt", "w")

    def generateTeamsListFromComp(fileList): # uses the match list to generate a list of teams that attended a comp, so that a second teamList is unnecessary
        uniqueTeams = []
        for row in fileList:
            teamsInRow = row[:4]
            for team in teamsInRow:
                if not team in uniqueTeams:
                    uniqueTeams.append(team)

        return uniqueTeams

    
    chart = api.getMatchList(compName, api.getCompInfo(compID, "1"))
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

    def getPowerScore(player): # master function, combines all the above functions to generate a powerScore value that reflects how "powerful" a team was in the competition
        matchDiffs = getListOfDiffs(player=player) # factor 1 (positive)
        allianceDiffs = getAllianceAverageDiffs(player=player) # factor 2 (negative)
        opponentDiffs = getOpponentAverageDiffs(player=player) # factor 3 (positive)
        matchPowers = []

        for index, matchDiff in enumerate(matchDiffs):
            matchPower = matchDiff - allianceDiffs[index] + opponentDiffs[index] # performs sigmoid calculation based on the 3 factors
            matchPowers.append(matchPower)
        
        powerScore = np.average(matchPowers)# / 2 + 0.5
        return round(powerScore * 1000) / 1000 # change to 10 outside the parentheses if need to revert
            
    ###### MAIN ######
    #print(teamList)
    for team in teamList: # changes each item in the team list to be a tuple of the team name and its powerScore as opposed to just the team name
        teamList[teamList.index(team)] = [team, getPowerScore(team)]

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

#runPowerScore()

team = "229V"
comps = api.getCompList(team)
#print(comps["meta"])
psList = []
#print(comps["data"])
for comp in range(comps["meta"]["total"]):
    #print(comps["data"][comp]["name"])
    #print(compPS)

    if len(comps["data"][comp]["divisions"]) == 1:
        try:
            fullPSLib, fullPSList = runPowerScore(comps["data"][comp]["name"], comps["data"][comp]["id"])
            #print(fullPS)
            compPS = fullPSLib[team]
            #compSum = sum(ps[1] for ps in fullPSList)
            #compWeight = log(0.51 * (compSum ** 0.225)) ** 2
            compWeight = 1.0 + 1 * ("Signature Event" in comps["data"][comp]["name"])
            psList.append([compPS, compWeight])
            #print([compPS, compSum, log(0.51 * (compSum ** 0.225)) ** 2])
        except:
            #print("This team deregistered from a comp")
            None

#matchPower = (2/(1 + exp(-0.05 * (matchDiff - allianceDiffs[index] + opponentDiffs[index])))) - 1 # performs sigmoid calculation based on the 3 factors
summation = 0
for x in psList:
    summation += x[0] * x[1]
print(team)# + " - " + str(round((((2/(1 + exp(-0.045 * (summation / len(psList))))) - 1) / 2 + 0.5) * 1000) / 10))
print(giveRanking(round((((2/(1 + exp(-0.045 * (summation / len(psList))))) - 1) / 2 + 0.5) * 1000) / 10))

    #print(comps["data"][comp]["id"])