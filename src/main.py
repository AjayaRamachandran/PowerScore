import numpy as np
from math import *
import inout as io
import api

###### ALGORITHM ######

def runPowerScore():
    output = open("output.txt", "w")

    def generateTeamsListFromComp(fileList): # uses the match list to generate a list of teams that attended a comp, so that a second teamList is unnecessary
        uniqueTeams = []
        for row in fileList:
            teamsInRow = row[:4]
            for team in teamsInRow:
                if not team in uniqueTeams:
                    uniqueTeams.append(team)

        return uniqueTeams

    compName, chart = api.getMatchList()
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
            matchPower = (2/(1 + exp(-0.05 * (matchDiff - allianceDiffs[index] + opponentDiffs[index])))) - 1 # performs sigmoid calculation based on the 3 factors
            matchPowers.append(matchPower)
        
        powerScore = np.average(matchPowers) / 2 + 0.5
        return round(powerScore * 1000) / 10
            
    ###### MAIN ######

    for team in teamList: # changes each item in the team list to be a tuple of the team name and its powerScore as opposed to just the team name
        teamList[teamList.index(team)] = [team, getPowerScore(team)]

    
    output.write(compName + " PowerScore\n")
    
    teamList.sort(key=lambda x: x[1], reverse=True) # sorts the list based on powerScore from largest to smallest
    for team in teamList:
        if team[0][0] != "#":
            output.write(f"{team[0]} \t {str(team[1])} \n") # writes output to a .txt file

    #print("Output has been saved to output.txt")
    io.showOutput("output.txt")

runPowerScore()