import requests
import time
from datetime import datetime

monthsLimits = [31,28,31,30,31,30,31,31,30,31,30,31]

API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMGQ0MWE0MWY2NTU0ZGViODM0MmUwOTdiOWM4MmYxYWIwZDFjNGFiNDAyOWMzNjcyMjA3NzVkOGI3MTFlYzZlZWYxMzcyYmQ0NWIzMjc5MWUiLCJpYXQiOjE3MDEzMDk0NjYuMzc3NDM1LCJuYmYiOjE3MDEzMDk0NjYuMzc3NDM4MSwiZXhwIjoyNjQ4MDgwNjY2LjM3MjA2ODksInN1YiI6IjEyNDE3MSIsInNjb3BlcyI6W119.DdBUax84hs2vZFKbXCexUiT-7J2BfTKjaVWwMIHOG_h5ph2A45aim7djnPhOBlPdUaUNxZF-s31de3IhlRMugXKaAADYjCojfrRDflLZfc3xJKDfsUJVSnU0gH-PdlRFrVhKrWtF4CYGW0EsLOsWCC_Klnf9RFv2kS50x0Ung0TqHCXyk7b5ejfGsHpRqJrilapAdN9P7nOV5JbN9b42LNTcJA8T-UlrrGiyb0nUGT9_WBL-WKyZQvdhrTU7iv1xXtivr-PaTjnEI_CpF-b8qqvvM4azIpaGNdxVfsNTF0-VH_6O3JKK-k9chcXgfw-INefHnRFsPlgJNgal6XvPweSipfJKK0WgC8VMX6Gnt3S7tCuJyYW5-EHNhPOjE6ANcsxaPd4ajQKjL60vxJixjsS502pbr8VOhIR_cVa_CtYZfK5T-TolGxnMSAlKV_4EJyr76wTZQN1MAiwZ03i3jWrFw--FDH5wk6wi2ttpit1o8Tp6H_3kd_2bakcdmezFE4Hv8gYG8jjIf6KYO5XiwPqYHHw3mmkyNTwitQpcErM_tzXCI_CELtO4Ztd60HZ-hAxWzn4POfxFWFUua_BU5-bi-fiWp5KzrpL0Je5oVFycFrGpO8L0Jb_6jgRZcFFc05WcJ4jlGn0-O6J1u2tosba_z3f3bfPMHD8RE8XnWow'
BASE_URL = 'https://www.robotevents.com/api/v2/'

def makeRequest(endpoint, params=None):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    response = requests.get(f'{BASE_URL}{endpoint}', headers=headers, params=params)

    if response.status_code == 200:
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
    endpoint = f'events?season%5B%5D=181&start=2023-08-03&end=2024-01-06&myEvents=false&eventTypes%5B%5D=tournament&per_page=250'
    pageMeta = makeRequest(endpoint, params=params)['meta']
    maxPages = pageMeta['last_page']
    compsPerPage = pageMeta['per_page']
    totalComps = pageMeta['total']

    compsIndex = []

    for page in range(maxPages):
        time.sleep(1)
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

def getMatchList(compName, matchData):

    matchList = []

    for matchNum in range(len(matchData)):
        alliances = matchData[matchNum]['alliances']
        blueScore = alliances[0]['score']
        redScore = alliances[1]['score']

        blueTeam1 = alliances[0]['teams'][0]['team']['name']
        blueTeam2 = alliances[0]['teams'][1]['team']['name']
        redTeam1 = alliances[1]['teams'][0]['team']['name']
        redTeam2 = alliances[1]['teams'][1]['team']['name']

        matchList.append([redTeam1, redTeam2, blueTeam1, blueTeam2, redScore, blueScore])

    #return compName[0], matchList
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
    endpoint = f'events?season%5B%5D=181'
    return makeRequest(endpoint=endpoint, params=params)