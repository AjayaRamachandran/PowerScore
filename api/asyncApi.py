###### IMPORT ######

import aiohttp
import asyncio
import random
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
from ast import literal_eval
from copy import deepcopy
import time

###### CONTROL ######
config = "api/config.txt"
debug = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("debug") - 5]
#-------------------#
if debug == "Y":
    import apiHandler
    import osEmul as os
    home = "http://localhost:5000"
    cred = credentials.Certificate("api/static/db/dbcache-507cd-firebase-adminsdk-srwcd-309135930e.json")
    
else:
    from api import apiHandler
    import os
    home = "https://powerscore.vercel.app"
    cred = credentials.Certificate(json.loads(os.environ.get('db')))

###### INITIALIZE ######

apiKeys = []
allKeys = []
usableKeys = []
for i in range(60):
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
        data = await response # this await line is what makes sure the task is only considered as complete when the data returns
        if response.status_code == 200:
            print("Received result")
            return data.json()
        else:
            print(f"Request failed with status code {data.status_code}")
            raise NameError
        #return data

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
    print(f"Sent request for {endpoint}, params:{params}")
    async with session.get(endpoint, params=params, headers=headers) as response:
        data = await response.json() # this await line is what makes sure the task is only considered as complete when the data returns
        return data['data']


###### ASYNCHRONOUS BATCHING FUNCTIONS ######

tomorrow = datetime.now() + timedelta(days=1)

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
    #print(comps)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for comp in range(len(compList)): # loops through every competition
            for division in range(len(comps[comp]["divisions"])): # loops through every division
                if datetime.strptime(comps[comp]["start"][:10], "%Y-%m-%d") > tomorrow:
                    print(f"{comps[comp]['name']} will occur in the future.")
                else:
                    task = fetch_comp(session, comps[comp]["id"], division + 1)
                    tasks.append(task) # adds the asynchronous task to a buffer

        results = await asyncio.gather(*tasks) # a "gate". this line of code only finishes when all the previously mentioned tasks are completed
        return results

###### PROCESSING FUNCTIONS ######

def checkTeamExistsInDivData(team, divData):
    divisionData = divData['ps']
    return team in divisionData
    #print(divisionData)

    #compList[index] = divisionData
    #inDivision = False
    #matchList = apiHandler.getMatchList("", divisionData)

    #for match in matchList:
        #if team in match[:4]:
            #return True
            #inDivision = True
            #break
    #if inDivision == False:
        #return False
        #print(f"Team is not in competition {divisionData[0]['event']['name']}, division {divisionData[0]['division']['name']}.")
        #divisionsToRemove.append(index)

firebase_admin.initialize_app(cred)
db = firestore.client()
teamsDocRef = db.collection('dbcache').document('OT5bu8pJ4yvZ05a2xJD3')

def purgeDB():
    """
    Purges the Firestore DB of the oldest XX competition entries.
    """
    @firestore.transactional
    def transactionUpdate(transaction):
        doc = teamsDocRef.get(transaction=transaction)
        
        docData = doc.to_dict()
        docRef = doc.reference

        fields_with_time = {
            field: value for field, value in docData.items()
            if isinstance(value, dict) and "time" in value
        }
        sorted_fields = sorted(fields_with_time.items(), key=lambda x: x[1]["time"])

        fieldsToDelete = [field for field, value in sorted_fields[:20]]
        if fieldsToDelete:
            updates = {field: None for field in fieldsToDelete}
            transaction.update(teamsDocRef, updates)

            print(f"Deleted fields {fieldsToDelete} in document {doc.id}")

    transactionUpdate(db.transaction())

def updateDB(competitionData):
    """
    Updates the Firestore DB to have all `locked` competition data.
    """
    global updateEnds
    ends = updateEnds

    for compNum in range(len(competitionData)):
        #print(competitionData[compNum])
        sku = competitionData[compNum]['sku']
        name = competitionData[compNum]['name']
        skuformatted = competitionData[compNum]['sku'].replace("-", "")
        div = competitionData[compNum]['data'][0]['div']
        print(ends)
        endDate = ends[sku][:10]

        # Parse the endDate and check if the competition is locked
        print(endDate)
        endDate = datetime.strptime(endDate, "%Y-%m-%d")
        yesterday = datetime.now() - timedelta(days=1)

        if endDate <= yesterday:
            teamsDocRef = db.collection('dbcache').document('OT5bu8pJ4yvZ05a2xJD3')

            # Define the transaction update function
            @firestore.transactional
            def transactionUpdate(transaction):
                doc = teamsDocRef.get(transaction=transaction)
                if doc.exists:
                    #data = doc.to_dict()
                    
                    transaction.update(teamsDocRef, {skuformatted : json.dumps({"time" : round(time.time()), "sku" : sku, "name" : name, "data" : [competitionData[compNum]["data"][0]]})})
                else:
                    print("DocError")
        
            # Execute the transaction
            transactionUpdate(db.transaction())
        else:
            print(f"Competition '{sku}' is not locked yet (endDate: {endDate}).")

def checkDB(competitionSKU, team):
    """
    Filters and returns a list of SKUs that do not exist in the Firestore DB for the given team.

    Args:
        `teamId (str)`: The team ID to check for competition SKUs.
        `competitionSKUs (list)`: A list of competition SKUs to check.

    Returns:
        `nonExistingSKUs (list)`: A list of SKUs that do not exist in the Firestore DB for the team.
    """

    try:
        @firestore.transactional
        def transactionUpdate(transaction):
            doc = teamsDocRef.get(transaction=transaction)
            if doc.exists:
                data = doc.to_dict()
                #print(str(data)[:100])
                #print(competitionSKU.replace("-", ""))
                if competitionSKU in str(data):
                    #print(str(data.get(competitionSKU.replace("-", "")))[:100])
                    #print()
                    divisionsInSKU = json.loads(data.get(competitionSKU.replace("-", "")))['data']
                    print(f'There is/are {len(divisionsInSKU)} division(s) in {json.loads(data.get(competitionSKU.replace("-", "")))["sku"]}.')
                    for div in divisionsInSKU:
                        status = checkTeamExistsInDivData(team, div)
                        if status:
                            print("200: Data was found in the DB.")
                            return {"sku": json.loads(data.get(competitionSKU.replace("-", "")))["sku"], "name" : json.loads(data.get(competitionSKU.replace("-", "")))["name"], "data" : [div]}
                    print("404 > DIV-ERR: Data was NOT FOUND in the DB.")
                    return "DivErr"
                else:
                    print("404 > COMP-ERR: Data was NOT FOUND in the DB.")
                    return "CompErr"
            else:
                print("666 > DOC-ERR: Document Error")
                return "DocErr"
        return transactionUpdate(db.transaction())
    except:
        return "DBFULL"


def getCompiledDataList(team, comps, season): # master function to return a full list of competitions' data in one request.
    apiHandler.setDefaultSeason(season)
    teamNameToFind = team

    #print(comps['data'])
    comp = comps['data'] # contains a list of competition basic info
    #print(f"Comp: {comp}")
    compSKUs = [{"sku" : competition['sku'], "end" : competition['end']} for competition in comp]
    onlyCompSKUs = [competition['sku'] for competition in comp]
    print(f"CompSKUs: {compSKUs}")
    print(f"OnlyCompSKUs: {onlyCompSKUs}")

    compList = []
    neededAPIComps = deepcopy(comp) # neededAPIComps preserves a copy of the TOTAL list of competitions (in generic format)

    yesterday = datetime.now() - timedelta(days=1)
    for compNum in range(len(comp)):
        if datetime.strptime(compSKUs[compNum]['end'][:10], "%Y-%m-%d") < yesterday:
            inDB = checkDB(compSKUs[compNum]['sku'], team)
            if not (inDB in ["DocErr","CompErr","DivErr","OtherErr","DBFULL"]):
                divData = inDB
                compList.append(divData)
    
    #print(f"Database has helped with: {compList}")
    #print(str(comp)) # comp now has a list of powerscore datas
    #for compN in range(len(neededAPIComps)):
        #for compM in range(len(compList)):
            #if compList[compM][0]['event']['code'] == neededAPIComps[compN]['sku']:
                #neededAPIComps[compN] = "delete"
                #break
    for compN in range(len(neededAPIComps)):
        for compM in range(len(compList)):
            #print(compList[compM])
            #print(neededAPIComps[compN]['sku'])
            if compList[compM]['sku'] == neededAPIComps[compN]['sku']:
                neededAPIComps[compN] = "delete"
                break


        #if neededAPIComps[compN]['sku'] in onlyCompSKUs:
            #neededAPIComps[compN] = "delete"
    iter = 0
    while "delete" in neededAPIComps and iter < 100:
        neededAPIComps.remove("delete")
        iter += 1
    #print(neededAPIComps)

    compListAppend = asyncio.run(getCompListAsync(teamNameToFind, neededAPIComps))

    global updateEnds
    updateEnds = {}

    iter = 0
    while [] in compListAppend and iter < 100:
        compListAppend.remove([])
        iter += 1

    for element in compListAppend:
        if element != []:
            compList.append(element)
            for sku in compSKUs:
                #print(f"ELEMENT: {element}")
                if element[0]['event']['code'] == sku['sku']:
                    updateEnds[sku['sku']] = sku['end']
                    break
    
    #print(len(compList))
    divisionsToRemove = []
    for index in range(len(compList)):
        if type(compList[index]) == list:
            divisionData = compList[index]

            compList[index] = divisionData
            inDivision = False
            matchList = apiHandler.getMatchList("", divisionData)

            for match in matchList:
                if teamNameToFind in match[:4]:
                    inDivision = True
                    break
            if inDivision == False:
                #print(f"Team is not in competition {divisionData[0]['event']['name']}, division {divisionData[0]['division']['name']}.")
                divisionsToRemove.append(index)

    for division in divisionsToRemove:
        compList.pop(division)
        #comp.pop(division)
        
        for divisionIndex in range(len(divisionsToRemove)):
            divisionsToRemove[divisionIndex] -= 1

    return compList