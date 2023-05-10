from datetime import date
import requests
import json
import xmltodict # used to convert xml files to JSON
 
courseJSONData = {"sessions": {}}

baseURL = "https://courses.students.ubc.ca/cs/servlets/SRVCourseSchedule?"
year = date.today().year
print(year)
term = "sesscd=${term}"
deptCode = "dept=${deptCode}"
LFSDepts = ['APBI', 'FNH', 'FOOD', 'FRE', 'GRS', 'HUNU', 'LFS', 'LWS', 'PLNT', 'SOIL']

def buildURL(year, term, dept):
    return f"{baseURL}&sessyr={year}&sesscd={term}&req=2&dept={dept}&output=3"

def getData(year, term):
    courses = {}
    for dept in LFSDepts:
        url = buildURL(year, term, dept)
        response_API = requests.get(url)
        data = response_API.text
        dept_courses_array = xmltodict.parse(data)["courses"]
        courses.update({f"{dept}":dept_courses_array})
    courseJSONData['sessions'].update({f"{year}{term}":courses})

# W: winter, S: Summer
# Maybe make this update every week or day to let the website load faster
# Add a try catch incase so we don't overwrite the current data
def updateData():
    getData(str(year), "W")
    getData(str(year), "S")
    getData(str(year - 1), "W")
    getData(str(year - 1), "S")
    getData(str(year + 1), "W")
    getData(str(year + 1), "S")

    with open("static/data/lfs-course-data.json", "w") as courseData:
        json.dump(courseJSONData, courseData, indent=4)
    courseData.close()