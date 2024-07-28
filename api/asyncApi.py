###### IMPORT ######

import aiohttp
import asyncio
import apiHandler
import random

###### CONTROL ######
config = "api/config.txt"
debug = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("debug") - 5]
#-------------------#
if debug == "Y":
    import osEmul as os
else:
    import os

###### INITIALIZE ######

apiKeys = []
allKeys = []
usableKeys = []
for i in range(50):
    apiKeys.append(os.environ.get(f'API_KEY{i + 1}'))
    usableKeys.append(i)
    allKeys.append(i)

BASE_URL = 'https://www.robotevents.com/api/v2/'


###### RETRIEVAL FUNCTIONS ######

async def fetch_division(session, comp_id, div): # pair test function with findDivisonAsync()
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
    endpoint = f"{BASE_URL}events/{comp_id}/divisions/{div}/rankings"
    params = {"per_page": "250"}
    async with session.get(endpoint, params=params, headers=headers) as response:
        data = await response.json() # this await line is what makes sure the task is only considered as complete when the data returns
        return data

async def fetch_comp(session, comp_id, div): # pair function with getCompListAsync(), retrieves a list of competition data using the RobotEvents API
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
    params = {
        "division": div,
        "round": "2",
        "per_page": "250"
    }

    endpoint = f'{BASE_URL}events/{comp_id}/divisions/{div}/matches?round%5B%5D=2'
    params = {"per_page": "250"}
    print(f"Sent request for {BASE_URL}{endpoint}, params:{params}")
    async with session.get(endpoint, params=params, headers=headers) as response:
        data = await response.json() # this await line is what makes sure the task is only considered as complete when the data returns
        return data


###### ASYNCHRONOUS BATCHING FUNCTIONS ######

async def findDivisionAsync(name, comp): # test function to retrieve the division of a team given the comp. first async test
    numDivs = comp["divisions"]
    if numDivs > 1:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for div in range(numDivs - 1):
                task = fetch_division(session, comp["id"], div + 1)
                tasks.append(task) # adds the asynchronous task to a buffer

            results = await asyncio.gather(*tasks) # a "gate". this line of code only finishes when all the previously mentioned tasks are completed

            for div, data in enumerate(results): # loops through each retrieved div to check if the team in question is in the division
                roster = [team["team"]["name"] for team in data["data"]]
                if name in roster:
                    return div + 1
    else:
        return 1

async def getCompListAsync(name, compList): # function to asynchronously retrieve a list of all the divisions of every competition a certain team has been to.
    comps = compList
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for comp in range(comps["meta"]["total"]): # loops through every competition
            for division in range(len(comps["data"][comp]["divisions"])): # loops through every division
                task = fetch_comp(session, comps["data"][comp]["id"], division + 1)
                tasks.append(task) # adds the asynchronous task to a buffer

        results = await asyncio.gather(*tasks) # a "gate". this line of code only finishes when all the previously mentioned tasks are completed
        return results


###### PROCESSING FUNCTIONS ######

def getCompiledDataList(team, compList, season): # master function to return a full list of competitions' data in one request.
    apiHandler.setDefaultSeason(season)
    team_name_to_find = team

    compList = asyncio.run(getCompListAsync(team_name_to_find, compList))
    divisionsToRemove = []
    for index in range(len(compList)):
        divisionData = compList[index]['data']

        compList[index] = divisionData
        inDivision = False
        matchList = apiHandler.getMatchList("", divisionData)

        for match in matchList:
            if team_name_to_find in match[:4]:
                inDivision = True
                break
        if inDivision == False:
            #print(f"Team is not in competition {divisionData[0]['event']['name']}, division {divisionData[0]['division']['name']}.")
            divisionsToRemove.append(index)

    for division in divisionsToRemove:
        compList.pop(division)
        
        for divisionIndex in range(len(divisionsToRemove)):
            divisionsToRemove[divisionIndex] -= 1
    return compList