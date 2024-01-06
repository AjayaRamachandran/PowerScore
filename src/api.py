import requests

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

def getTeamID(name, params):
    endpoint = f'teams?'
    return makeRequest(endpoint, params=params)['data'][0]['organization']

params = {
    "number": "8568A",
    "grade": "High School"
    }

print(getTeamID("8568A", params))