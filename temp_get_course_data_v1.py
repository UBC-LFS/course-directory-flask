# Get courses from the old API - no longer works
from datetime import date
import requests
import json
import xmltodict # used to convert xml files to JSON
import os
import time

courseJSONData = {"sessions": {}}

baseURL = "https://courses.students.ubc.ca/cs/servlets/SRVCourseSchedule?"
year = date.today().year
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

        # Ensures that there are courses in the array, if not, do not add courses to set
        if (dept_courses_array is not None):
            for course in dept_courses_array["course"]:
                # Grabs the necessary variables to build the syllabus URL
                syllabusTerm, originalCourseName = hasSyllabus(f"{dept} {str(course['@key'])}", syllabusInfo)
                # Adds the variables to the dictionary
                course["@syllabusTerm"] = str(syllabusTerm)
                course["@originalCourseName"] = str(originalCourseName)
            # Adds the array of courses in that department to the courses dictionary
            courses.update({f"{dept}":dept_courses_array})
    
    # If there are courses in that session, add it to the set of courses
    if (len(courses) > 0):
        # Backup the courses for that session
        try:
            with open(f"static/data/backedUpSessions/{year}{term}.json", "w") as sessionData:
                json.dump({f"{year}{term}":courses}, sessionData, indent=4)
        except:
            print("Could not back up session data")
            
        courseJSONData['sessions'].update({f"{year}{term}":courses})

# W: winter, S: Summer
def updateData():
    getData(str(year + 1), "W")
    getData(str(year + 1), "S")
    getData(str(year), "W")
    getData(str(year), "S")
    getData(str(year - 1), "W")
    getData(str(year - 1), "S")
    try:
        with open("static/data/lfs-course-data.json", "r") as courseData:
            currentSavedJSONData = json.loads(courseData.read())
        # If current data is valid, then back it up
        if (currentSavedJSONData is dict):
            with open("static/data/lfs-course-data-backup.json", "w") as courseData:
                json.dump(currentSavedJSONData, courseData, indent=4)
                print(f'Backed up data: {time.strftime("%A, %d. %B %Y %I:%M:%S %p")}')
    except:
        print("Data failed to back up. Stopping data update.")
        print("Data failed to update. Reverting data update.")
        with open("static/data/lfs-course-data-backup.json", "r") as courseData:
            backedUpJSONData = json.loads(courseData.read())
            courseData.close()
        with open("static/data/lfs-course-data.json", "w") as courseData:
            json.dump(backedUpJSONData, courseData, indent=4)
            print(f'Finished reverting data at: {time.strftime("%A, %d. %B %Y %I:%M:%S %p")}')
            courseData.close()
        return
    
    # If data successfully backs up
    try:
        with open("static/data/lfs-course-data.json", "w") as courseData:
            json.dump(courseJSONData, courseData, indent=4)
            print(f'Data updated at: {time.strftime("%A, %d. %B %Y %I:%M:%S %p")}')
        courseData.close()
    except:
        print("Data failed to update. Reverting data update.")
        with open("static/data/lfs-course-data-backup.json", "r") as courseData:
            backedUpJSONData = json.loads(courseData.read())
            courseData.close()
        with open("static/data/lfs-course-data.json", "w") as courseData:
            json.dump(backedUpJSONData, courseData, indent=4)
            print(f'Finished reverting data at: {time.strftime("%A, %d. %B %Y %I:%M:%S %p")}')
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