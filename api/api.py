import requests
import time
from datetime import datetime

monthsLimits = [31,28,31,30,31,30,31,31,30,31,30,31]
apiKeys = []
API_KEY1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMGQ0MWE0MWY2NTU0ZGViODM0MmUwOTdiOWM4MmYxYWIwZDFjNGFiNDAyOWMzNjcyMjA3NzVkOGI3MTFlYzZlZWYxMzcyYmQ0NWIzMjc5MWUiLCJpYXQiOjE3MDEzMDk0NjYuMzc3NDM1LCJuYmYiOjE3MDEzMDk0NjYuMzc3NDM4MSwiZXhwIjoyNjQ4MDgwNjY2LjM3MjA2ODksInN1YiI6IjEyNDE3MSIsInNjb3BlcyI6W119.DdBUax84hs2vZFKbXCexUiT-7J2BfTKjaVWwMIHOG_h5ph2A45aim7djnPhOBlPdUaUNxZF-s31de3IhlRMugXKaAADYjCojfrRDflLZfc3xJKDfsUJVSnU0gH-PdlRFrVhKrWtF4CYGW0EsLOsWCC_Klnf9RFv2kS50x0Ung0TqHCXyk7b5ejfGsHpRqJrilapAdN9P7nOV5JbN9b42LNTcJA8T-UlrrGiyb0nUGT9_WBL-WKyZQvdhrTU7iv1xXtivr-PaTjnEI_CpF-b8qqvvM4azIpaGNdxVfsNTF0-VH_6O3JKK-k9chcXgfw-INefHnRFsPlgJNgal6XvPweSipfJKK0WgC8VMX6Gnt3S7tCuJyYW5-EHNhPOjE6ANcsxaPd4ajQKjL60vxJixjsS502pbr8VOhIR_cVa_CtYZfK5T-TolGxnMSAlKV_4EJyr76wTZQN1MAiwZ03i3jWrFw--FDH5wk6wi2ttpit1o8Tp6H_3kd_2bakcdmezFE4Hv8gYG8jjIf6KYO5XiwPqYHHw3mmkyNTwitQpcErM_tzXCI_CELtO4Ztd60HZ-hAxWzn4POfxFWFUua_BU5-bi-fiWp5KzrpL0Je5oVFycFrGpO8L0Jb_6jgRZcFFc05WcJ4jlGn0-O6J1u2tosba_z3f3bfPMHD8RE8XnWow'
apiKeys.append(API_KEY1)
API_KEY2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMDhlODA3N2NiMzYxMGFjMWYzYjFjOTc0ZDIyOGM4ZDUyMDRiOGUzYmVkYjQ5NWVjMTczNjllMDY4MDA1NTMwNDZlMjZkOGMwNWYxMGZlYWEiLCJpYXQiOjE3MTgzMTA5NTAuMjUxNTIxMSwibmJmIjoxNzE4MzEwOTUwLjI1MTUyNCwiZXhwIjoyNjY0OTk5MzUwLjI0NTM0MDgsInN1YiI6IjEzMDg2MiIsInNjb3BlcyI6W119.c5G-kn5dKYsIotL5CHlFAeloUHpvg9d5LpSPVA4ujCNrpc0-N_MOr_a7tzh1_HfpveXPv9ffm67TyhcS3ubApJ6aTNXnTxkFOqXyWz4x6VSSoBIUCQKQx9JuJFf8dTVffOBHiB99eT-WKtNiJtZuenRU9uqK_npjq5f2zphIIN28JXHoR05lQNi8LLuANUcV68nhyFd2aEHj5FTh5l3HCbwL_U6l8LnmLy3pNQ_LK8P5a9zV7o-e581eHCUKf4_K7316x4iEgI_xTilveh8JpV90lZO9er9axQDorv55SDQ2VI8RjRZZCmgkK97Jp6DLHkA24T1pFv7K_cwQCUamoKfNCQ-9yzyEiwjhrDR74lsQw7yAKZdNp5hH0qKpCn_EJLgPSRPunGDN72YiDgQQxZt0bnvToYcScy2QZGDoyh4Mc3A8FmP3WQFtaQAwJuLMflO-TtN-wWme-J_4FhbStwwVE4WTudAZ4fKobW6w2qsNahnBFZhW4qFQmWNMxilev2AHsWIarC8GKsNVNSaieCajxTe4DYKF7OOL2GQxuiNtfgnApQRDIABr0LZlkRyeSzdYKlgZuH0k03XhodQJTfV__2x__dfDVVJF9qq5-nSrkEi4roMlz6g7gVOQrP8v8MPfgEwjz0bIwpuTN1crnqeXYFRx3IGtQqdlKbZfkjk'
apiKeys.append(API_KEY2)
API_KEY3 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiYmU5NjdhNGQ1MzY4ZTFlYmE2ODJkNjNjOGM2ZTdjNGRmNzE0YzRlNGE3NmI3OTQ3ZGU2MTkxYjhjMTE0MjMzMDBkZDhhMzcxMDk0YWVhMDIiLCJpYXQiOjE3MTgzMTEwNjUuMzI1NzEwMSwibmJmIjoxNzE4MzExMDY1LjMyNTcxMjksImV4cCI6MjY2NDk5OTQ2NS4zMTgyMjAxLCJzdWIiOiIxMzA4NjIiLCJzY29wZXMiOltdfQ.GsXOmRbMm83c1gFS2VKWycGoTyjjWX3SR5CvlIkQlzZCBzfLTDJNwb2h0xJ0cfbf1m2DbmQmnHmpn0-2BvR-8JMDLCmV5bijyXTjsOI6ElMEOC9jVU3mP80YYVkKzU6XINfDAKkcmcORWMs5RQJYm1z1UUh_7gjLkiEz87_ZmkW_FDi13xz5m3LPsCo-8C-EzOzA1fVLmntp11XmQ1uRy_iuGat7QDFaSRqW9CdfEl-jzIvlMNsamAoXKmdj9z1uzCyWhVUwlg_39NEg9XqKG4I3_OeKbyrAYWr3L6UVZYTRIhANyRXo58rvw161yUDORtYdQ4cr7zyltzWVCFic-7eXQed-JFBtdwgnIcah-jspJMMnntEZFxr6NbssS9UPm5Hz1A6GX8rUlpgVRd9UZmxueXXbM1lNrJUTG6XJrHdTr-egCbSTdaFndvaqm6HRT5cQahhPujIWlHaJB1C0Q3ey8bAO6zsMt8A1QkxXOJhGA22cWjt8hmSVFPGrNU3JRLRKS5-dMjJlRPSuHlYtihEKpk3yNkr1UOPvOjXhB0amCKGs-fT51vfMphXnRFHeiPNh3QKW4qxOCKoVWS8MBn8Cthjvj4PyJ_vTs20QkMSBk8E_xIKlxe1_RtNGpT_OLYlNGJnu4AjAQrtixYj26Z-PLqnuhAwbzoPKq69qOq4'
apiKeys.append(API_KEY3)
API_KEY4 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiOTJkMTBhYmRiMzllZWFlOGM1ZmUxZGZlMmVmOTRmY2I5NjY5OTIxOWEzZmNkZDMxYzBiMzU0MDEyMDk0NmFiNTNkNmIxNDY4MzdiOGRhYTUiLCJpYXQiOjE3MTgzMTIxNjMuNDY0MjYxMSwibmJmIjoxNzE4MzEyMTYzLjQ2NDI2NTEsImV4cCI6MjY2NTAwMDU2My40NTg2OTQsInN1YiI6IjEzMDg2MiIsInNjb3BlcyI6W119.qe0zDv-vrFNNtvscbTfdbMDhYz9Rs1XGSEFDQTLQk_0AHMY9wm1UT0ADIJ7CPWtaRBRY1kyuyuO3AkiyrHCwFXFtKqdt1laRe1NShSdf9n0Dv2q4kagbcJQg-Lerx6FA4FKKDfJNzHXE31MT7wlN9PMkhL821Wh7DOX5u8Aa4exgaPq4WBDNdlPzS9mD2sy9LOKsVOTvAlOtam3CXWi5dVwE6JgXe17YE_hZkQupwBEgd59HDIhbH4a7z4c540Ahov0CPSqQgHxswAHaJC-A2j3EtLKuFAUNx6G6LwePb08N1BZ619g2FzhucRsuKzNwsibYX0rkUQixOkVGsKlKXo1iav2kZcrWtFs4a1Hgu6WiQt5Hgg-8b4waK0vYAwkAai2Odg9S_6UhQto13Zmt5nqDoY_zLIOoG9KxzH2ePE0XKlZ8TIIOlcILCWqt7mHwwil3HlUSqvvNikvytGT-9jatwSzJi_-lLqNNoh6hz6BgZ07lKE9qCaV9hzGZD_klOFussUk7YCEMEIjE6JGMEycbA1ntCO2aQw5iMmhyiDwLQ7c281j6EgqUA9MYIsdWAakfK4Eyc2vkzNUkZgBybdtqKjiSJEgmjVBiAj-uLWKnIfwYsRlGCd4MmGuQLV_0DwFwG3PbHkNVv3cDAMcMoIk-vhLjvp9H3UzfTzvOhD8'
apiKeys.append(API_KEY4)
API_KEY5 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMjA4NjY0N2UyNmExODg3YWUyNDA5MGEwMWIyMzk3Nzc2NmQxYmE3MzRiZjVmY2U0MDE4ZjI5MjVkYzg0YzY5ODg1MTdjZTgyMDcxYjU0MGIiLCJpYXQiOjE3MTgzMTIxOTkuNDM1NzUxLCJuYmYiOjE3MTgzMTIxOTkuNDM1NzU0MSwiZXhwIjoyNjY1MDAwNTk5LjQzMDIwOTIsInN1YiI6IjEzMDg2MiIsInNjb3BlcyI6W119.lP9UsLPU35xz0D1wG2UxC1c5IRwetxumrRkog3mb2PXHr4iGvLxh66ytrCmaVPE8y5yx0Fpml7RdPwTbY-Cd8z5OUg-DCAG2aTWmxvdnGKMeKF1zmczUt3I5auaz-xlphPX3Wpie0gDgQmJiwRGbOEDj2GuJttJRmKJdVggHcXmD6rUUr955O8S40HmX3_apDjJyx45cLbfCrM1TBpyqdQ59D1lizgQElhzxmh7Sppfwmce0WjdxzUHNaP-2myx16RfkBpSBQy89uU7NcXYUmiaW_pcatFpHdR6HSwrXk2UsBSLl6KXHpGHJS4aIFV8HztY3Au6LWt5Q1yvS07il1Bu_XR4cAAJGtUevh4CAZkKygYM0qJIhA0tjj9Np_HdncbnbKkvAnvLF4Dpu72WC_bjdbn_37Q3wcZ9_xsY7IucoO5m1-10LbDU9l15zskJJVntX4sN9IizRzM4le1437pzkcFqhH8I7lDO-7hYSw0BrVcOSNoUvJ2oprq2Rg3vOyEXNgcwCjtwVmw6nI6Fb6kGjCAEhefRpoOqbFsnF3J4re8jEWANihwu_Upwj93HxClcWnL9M3diwECweI-U_x9xFo3v4k0B_yfKrb3Nsi-H2TRexyHag2tFWIUNz8xTw4wPcyVAKMPqauR73C1Hp2imbgX3xrKcqulTuRvj9hAY'
apiKeys.append(API_KEY5)
API_KEY6 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiNDlkMDIwZTlhZjZmNDMyOTIyN2MwZjZjZDRkYTI0MWFmYWJkNjUxYjI1ZTZjNjlhNmEyZDgzNTBkMmYzYTg3OWFiOTI5NzdkMzNhZWUxZTYiLCJpYXQiOjE3MTgzMTIyNzEuOTgwMDc2MSwibmJmIjoxNzE4MzEyMjcxLjk4MDA3ODksImV4cCI6MjY2NTAwMDY3MS45NzQ5NzgsInN1YiI6IjEzMDg2MiIsInNjb3BlcyI6W119.QTTzSkdVNXB9DyMjIsNEQlOH6dByuHMEJdDc51cpbvys9vig0WNQ6XgSJrLAiLUnkxEZZxvEa0owTS46uNEbTs7M8NtAK17_4JXQ-Seer-jjVZi6_6VhxMT0OjHD5BJzM0IXbuYV4hbxq8IvMqlqqck-ipnIcwh_Vk5DyYLX7b1QpzZb47uDW0NXOmfReooTg-8T3u5mdsq0mRsmAfHnTPJCs784OZbg1KnW163_CINWumelg_p7YrXpqNfLx3128nJ7W5nZUIY2jeD2291At3yJhrfh6STVtTi4_gUp9q7l6kZ_qQzr_AbCeQ0fa6iwoAGF9JMioCHwPx6ZTQxrmVe4J8ltVnN30zikHch79xPDY3VM-tUsQgds7fRVu8lgWVaZqrWpUnNacfxuAVk3wijdmKBOKKZqkXM7fh2I5v2RvFHH5mPT3-SMf7K0hg1bn5s32nM93M_pLf3QMMRfVV0aWkxPbIzTL68igmOv-Vrtr9WXYrMbpfFzDd16bLVAxrHPXeL2nFzS5KeUiMjzRxYrYl_l1Zb3DfaORy0Af7iyx6EYsfoh-LaKisTYU7wehb7ZGjTyFjYXFPmppTo4MftELKg8bblukHJWCLJKxcmv13eX3M6AaIZGk3ThrfOi_auNntXwzRSx7VVWIklGB_CiJKqPDT2Y_y4c1rWiii4'
apiKeys.append(API_KEY6)
API_KEY7 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiY2Q2MTAwZWRkMmRmZTI5MGZjYTdiZWY1ODE1M2Y1MTIxYzIxZGM2ZDA2ZGU0N2Y1NGQwYWZmM2Y4NDFkNTk1ZjZkNjkwNjg4YTAxNjJjMGQiLCJpYXQiOjE3MTgzMTIzMDYuMTAxNjU4MSwibmJmIjoxNzE4MzEyMzA2LjEwMTY2MTksImV4cCI6MjY2NTAwMDcwNi4wODg3NzI4LCJzdWIiOiIxMzA4NjIiLCJzY29wZXMiOltdfQ.I1hdCQxWF9Y-4H3gZa4Sveik824l4vk6Oj9r9f19gTlY_8r8iF2IG8fHGnVrrlLOVGQTzbtVgF9tKAmGSk_R7EU0RbRdY-3tBMdvFni_dUcEN55QpcB4QIq05R7NY1QIqg1uh67oTLDjRo4be1Vhc9zECcvHkj3tMG-YbOfWQPn4Urb-EPHuQUOlBZOkIIUZaztSK6D0GGSp9_hqr3NG3au3Uob2UIuO4FpAByVM68cKCwq0sDzG_FcSnmhLME7MUIS23tHBlgNAEeAk1NOp1vVBnyoZwm7k7EoMlSZqqIq0aJBYlL9QX1xIsTCAbtiGrFr7-30PYuT58kojz4RoXFt8OQL3uMu9VjLIttl71qf0fsvAUk3nWhaaBEh8fnwwHp7QTVah0KKdnn170v3qbkPLFjCgdf2gnEp3Zj--a3gDbOvTiPftARgIhgyfP8kJTV9gAFxXNc-bRQKS2msFNNTqJvzY6czDFSBeDYXPIN3RaHah3zaYnexVRdmiqQqSDg96pp2tMgPUj9PIqf062xpdZc3ANGiiCVIBMdMdS56FPfHDqHfVAldK2AJ_raVR0bT36Uj2-1iw_c1izZi-TM_Cn6gQrx0TN0W5aGQ2YDVSl0iyFz4jTLo98lRu7h7jFwcHaofRP4wLsb7Nhw57bUVv2Bj3QtsTPCdpPFK_t-c'
apiKeys.append(API_KEY7)
requestNumber = 0

BASE_URL = 'https://www.robotevents.com/api/v2/'

def makeRequest(endpoint, params=None):
    global requestNumber
    headers = {
        'Authorization': f'Bearer {apiKeys[requestNumber%3]}',
        'Content-Type': 'application/json',
    }

    requestNumber += 1
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
    endpoint = f'events?season%5B%5D=181&start=2023-08-03&end=2024-01-06&myEvents=false&eventTypes%5B%5D=tournament&per_page=250'
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

    for matchNum in range(len(matchData)):
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
    endpoint = f'events?season%5B%5D=181'
    return makeRequest(endpoint=endpoint, params=params)