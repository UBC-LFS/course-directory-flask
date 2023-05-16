from datetime import date
import requests
import json
import xmltodict # used to convert xml files to JSON
import os

courseJSONData = {"sessions": {}}

baseURL = "https://courses.students.ubc.ca/cs/servlets/SRVCourseSchedule?"
year = date.today().year
print(year)
term = "sesscd=${term}"
deptCode = "dept=${deptCode}"
LFSDepts = ['APBI', 'FNH', 'FOOD', 'FRE', 'GRS', 'HUNU', 'LFS', 'LWS', 'PLNT', 'SOIL']

def buildURL(year, term, dept):
    return f"{baseURL}&sessyr={year}&sesscd={term}&req=2&dept={dept}&output=3"

# Returns the variables necessary to build the course syllabus URL
def hasSyllabus(courseName, syllabusInfo):
    for term in syllabusInfo:
        for course in term["courses"]:
            if (courseName in course):
                return term["term"], course
    return "", ""

def getData(year, term):
    courses = {}

    """ Old method: fetched data from a different website, but we want to store the syllabuses in this one instead
    # Gets the list of courses with a syllabus
    syllabusInfo = list(json.loads(fetchDataAsText("https://prod-lc01-pub.landfood.ubc.ca/lfscourses/availableSyllabi")))
    # Reverse list so the most recent years are at the top
    syllabusInfo.reverse()
    """
    syllabusInfo = getCoursesWithSyllabus()

    for dept in LFSDepts:
        url = buildURL(year, term, dept)
        response_API = requests.get(url)
        data = response_API.text
        dept_courses_array = xmltodict.parse(data)["courses"]
        # Fixes the error where departments with only 1 course uses a dict instead of an array -> results in undefined classes on Frontend
        try:
            if (type(xmltodict.parse(data)["courses"]["course"]) is dict):
                dept_courses_array = {"course": [xmltodict.parse(data)["courses"]["course"]]}
        except:
            pass
        
        # Grabs syllabus for the courses
        if (dept_courses_array is not None): # Ensures that there are courses in the array
            for course in dept_courses_array["course"]:
                # Grabs the necessary variables to build the syllabus URL
                syllabusTerm, originalCourseName = hasSyllabus(f"{dept} {str(course['@key'])}", syllabusInfo)
                # Adds the variables to the dictionary
                course["@syllabusTerm"] = str(syllabusTerm)
                course["@originalCourseName"] = str(originalCourseName)
        # Adds the array of courses in that department to the courses dictionary
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

def fetchDataAsText(url):
    response_API = requests.get(url)
    return response_API.text

# Looks at courseDirectory and returns an array of courses with a syllabus
def getCoursesWithSyllabus():
    coursesWithSyllabus = []
    courseDirectory = "templates/CourseDirectory"
    for subFolder in os.listdir(courseDirectory):
        sessionFolder = courseDirectory + "/" + subFolder
        # If the directory exist
        if os.path.isdir(sessionFolder):
            sessionWithSyllabus = {
                "term": subFolder,
                "courses": []
            }
            for originalCourseName in os.listdir(sessionFolder):
                sessionSubFolder = sessionFolder + "/" + originalCourseName
                # If the directory exist
                if os.path.isdir(sessionSubFolder):
                    sessionWithSyllabus["courses"].append(originalCourseName)
            coursesWithSyllabus.append(sessionWithSyllabus)
    return coursesWithSyllabus
            


            

