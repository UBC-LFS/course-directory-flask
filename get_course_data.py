import requests
import json
import xmltodict # used to convert xml files to JSON
 
courseJSONData = {"sessions": []}

baseURL = "https://courses.students.ubc.ca/cs/servlets/SRVCourseSchedule?"
year = 2023
term = "sesscd=${term}"
deptCode = "dept=${deptCode}"
LFSDepts = ['APBI', 'FNH', 'FOOD', 'FRE', 'GRS', 'HUNU', 'LFS', 'LWS', 'PLNT', 'SOIL']

def buildURL(year, term, dept):
    return f"{baseURL}&sessyr={year}&sesscd={term}&req=2&dept={dept}&output=3"

def getData(year, term):
    courses = []
    for dept in LFSDepts:
        url = buildURL(year, term, dept)
        response_API = requests.get(url)
        data = response_API.text
        data_dict = xmltodict.parse(data)
        courses.append(data_dict)
    courseJSONData['sessions'].append({f"{year}{term}": courses})

# W: winter, S: Summer
# Maybe make this update every week or day to let the website load faster
def saveData():
    getData("2023", "W")
    getData("2022", "W")
    getData("2024", "W")
    getData("2023", "S")
    getData("2022", "S")
    getData("2024", "S")
    with open("static/data/lfs-course-data.json", "w") as courseData:
        json.dump(courseJSONData, courseData, indent=4)
    courseData.close()

saveData()