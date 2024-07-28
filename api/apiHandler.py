import requests
import random

###### CONTROL ######
config = "api/config.txt"
debug = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("debug") - 5]
#-------------------#
if debug == "Y":
    import osEmul as os
else:
    import os
from datetime import datetime

monthsLimits = [31,28,31,30,31,30,31,31,30,31,30,31]
apiKeys = []
allKeys = []
usableKeys = []
for i in range(50):
    apiKeys.append(os.environ.get(f'API_KEY{i + 1}'))
    usableKeys.append(i)
    allKeys.append(i)

BASE_URL = 'https://www.robotevents.com/api/v2/'
defaultSeason = ""

def setDefaultSeason(season):
    global defaultSeason
    defaultSeason = season

def makeRequest(endpoint, params=None):
    global requestNumber, usableKeys, allKeys, apiKeys
    if len(usableKeys) == 0:
        usableKeys = allKeys.copy()
    else:
        requestNumber = random.choice(usableKeys)
        usableKeys.remove(requestNumber)
    headers = {
        'Authorization': f'Bearer {apiKeys[requestNumber]}',
        'Content-Type': 'application/json',
    }

    print(f"Sent request for {BASE_URL}{endpoint}, params:{params}")
    response = requests.get(f'{BASE_URL}{endpoint}', headers=headers, params=params)

    if response.status_code == 200:
        print("Received result")
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        return None


###### SUBFUNCTIONS ######

def getDistance(string1, string2): # function to return the score of how close two strings are, used to rank results of search
    if len(string1) < len(string2):
        string2 = string2[:len(string1)]
    elif len(string1) > len(string2):
        string1 = string1[:len(string2)]

    score = 0
    for letter in range(len(string1)):
        if string2[letter] in string1:
            score += 1
            if string2[letter] == string1[letter]:
                score += 3

    return score

def getTeamInfo(params, info): # gets info of a team (test)
    endpoint = f'teams?'
    return makeRequest(endpoint, params=params)['data'][0][info]

def getEventList(params=None): # gets a list of all vrc over under comps that have happened so far
    endpoint = f'events?season%5B%5D={defaultSeason}&start=2023-08-03&end=2024-01-06&myEvents=false&eventTypes%5B%5D=tournament&per_page=250'
    pageMeta = makeRequest(endpoint, params=params)['meta']
    maxPages = pageMeta['last_page']
    compsPerPage = pageMeta['per_page']
    totalComps = pageMeta['total']

    compsIndex = []

    for page in range(maxPages):
        #time.sleep(0.33)
        pageTag = f"&page={page+1}"

        pageData = makeRequest(endpoint=endpoint+pageTag, params=params)['data']

        for comp in range(compsPerPage):
            if page + 1 == maxPages:
                if comp < totalComps % compsPerPage - 1:
                    compsIndex.append(
                        [
                            pageData[comp]["name"],
                            pageData[comp]["id"]
                        ]
                    )
                    #print(f"Comp {comp + 1} of page {page + 1} requested")
            else:
                compsIndex.append(
                    [
                        pageData[comp]["name"],
                        pageData[comp]["id"]
                    ]
                )
                #print(f"Comp {comp + 1} of page {page + 1} requested")
    return compsIndex

def getCompInfo(ID, division):
    params = {
    "division": division,
    "round": "2",
    "per_page": "250"
    }

    endpoint = f'events/{ID}/divisions/{division}/matches?round%5B%5D=2'

    return makeRequest(endpoint=endpoint, params=params)['data']

def getCompInfoBySKU(sku, div):
    params = {
        "per_page": "250"
    }

    endpoint = f"events?sku%5B%5D={sku}&myEvents=false"
    data = makeRequest(endpoint=endpoint, params=params)['data'][0]
    name = data['name']
    numDivs = len(data['divisions'])
    ID = data['id']

    divisionNames = []
    for division in data['divisions']:
        divisionNames.append(division['name'])

    divisionsData = []

    '''for div in range(numDivs):
        params = {
            "division": str(div + 1),
            "per_page": "250",
            "round": "2"
        }
        endpoint = f"events/{ID}/divisions/{div+1}/matches"
        divisionsData.append(makeRequest(endpoint=endpoint, params=params)['data'])'''
    
    params = {
        "division": str(div),
        "per_page": "250",
        "round": "2"
    }
    endpoint = f"events/{ID}/divisions/{div+1}/matches"
    divisionsData.append(makeRequest(endpoint=endpoint, params=params)['data'])

    return name, divisionsData, divisionNames

def getMatchList(compName, matchData):
    matchList = []
    #print(matchData)
    for matchNum in range(len(matchData)):
        #print(matchData[matchNum])
        alliances = matchData[matchNum]['alliances']
        blueScore = alliances[0]['score']
        redScore = alliances[1]['score']

        blueTeam1 = alliances[0]['teams'][0]['team']['name']
        blueTeam2 = alliances[0]['teams'][1]['team']['name']
        redTeam1 = alliances[1]['teams'][0]['team']['name']
        redTeam2 = alliances[1]['teams'][1]['team']['name']

        matchList.append([redTeam1, redTeam2, blueTeam1, blueTeam2, redScore, blueScore])

    return matchList

def askUserForComp():
    if datetime.now().day > monthsLimits[datetime.now().month]:
        currentDay = 1
        currentMonth = datetime.now().month + 1
    else:
        currentDay = datetime.now().day + 1
        currentMonth = datetime.now().month

    params = {
        "season": "181",
        "start": "2023-08-03",
        "end": f"{datetime.now().year}-{currentMonth}-{currentDay}",
        "event_types": "tournament",
        "per_page": "250"
    }

    compsIndex = getEventList(params=params)

    competition = input("What competition do you want to analyze? ")

    for comp in range(len(compsIndex)): # gets the score of all the comps based on how close they are to the inputted prompt
        score = getDistance(competition, compsIndex[comp][0])
        compsIndex[comp] = [compsIndex[comp][0], compsIndex[comp][1], score]
    
    compsIndex.sort(key=lambda x: x[2], reverse=True) # sorts the list based on pseudo-levenshtein distance (better versionn for this purpose), smallest first

    confirm = "n"
    listItem = 0
    while confirm == "n": # repeatedly goes down the list until the user claims their search is satisfied
        confirm = input(f"Did you mean {compsIndex[listItem][0]}? (y/n) ")
        if confirm == "n":
            listItem += 1
    
    compName = compsIndex[listItem]
    matchData = getCompInfo(compsIndex[listItem][1], "1")
    getMatchList(compName, matchData)


def getCompList(team):
    teamID = makeRequest(endpoint=f"teams?number%5B%5D={team}&grade%5B%5D=High%20School&myTeams=false",params={})["data"][0]["id"]

    params = {
    "team": teamID,
    "per_page": "250"
    }
    endpoint = f'events?season%5B%5D={defaultSeason}'
    return makeRequest(endpoint=endpoint, params=params)