import requests
import json
import xmltodict # used to convert xml files to JSON
 

baseURL = "https://courses.students.ubc.ca/cs/servlets/SRVCourseSchedule?"
year = 2023
term = "sesscd=${term}"
deptCode = "dept=${deptCode}"
LFSDepts = ['APBI', 'FNH', 'FOOD', 'FRE', 'GRS', 'HUNU', 'LFS', 'LWS', 'PLNT', 'SOIL']

def buildURL(year, term, dept):
    return f"{baseURL}&sessyr={year}&sesscd={term}&req=2&dept={dept}&output=3"


def getData(year, term):
    for dept in LFSDepts:
        url = buildURL(year, term, dept)
        response_API = requests.get(url)
        data = response_API.text
        data_dict = xmltodict.parse(data)
        print(data_dict["courses"])

# W: winter, S: Summer
# getData("2023", "W")
# getData("2022", "W")
# getData("2024", "W")
# getData("2023", "S")
# getData("2022", "S")
# getData("2024", "S")