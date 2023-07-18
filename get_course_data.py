from datetime import date
import requests
import json
import xmltodict  # used to convert xml files to JSON
import os
from dotenv import load_dotenv
import time

load_dotenv()
# Loads API tokens
clientID = os.getenv("CLIENT-ID")
clientSecret = os.getenv("CLIENT-SECRET")

courseJSONData = {"sessions": {}}
year = date.today().year

LFSDepts = ['APBI', 'FNH', 'FOOD', 'FRE',
            'GRS', 'HUNU', 'LFS', 'LWS', 'PLNT', 'SOIL']

# Returns the variables necessary to build the course syllabus URL


def hasSyllabus(courseName, syllabusInfo):
    for term in syllabusInfo:
        for course in term["courses"]:
            if (courseName in course):
                return term["term"], course
    return "", ""


def courseOneIsHigher(courseOne, courseTwo):
    return (courseOne["@key"] > courseTwo["@key"])


def getData(year, term):
    courses = {}
    syllabusInfo = getCoursesWithSyllabus()

    for dept in LFSDepts:
        url = f"https://sat.api.ubc.ca/academic-exp/v1/course-section-details?academicYear={year}&courseSubject={dept}_V&page=1&pageSize=500"
        data = requests.get(
            url,
            headers={"x-client-id": clientID, "x-client-secret": clientSecret}
        ).text
        deptCourseData = json.loads(data)['pageItems']

        dept_courses_array = []
        # Ensures that there are courses in the array, if not, do not add courses to set
        if (len(deptCourseData) > 0):
            for course in deptCourseData:
                # if term matches course and the course is open
                if (term == course["academicPeriod"]["academicPeriodName"].split(" ")[1][0] and ("Open" == course["sectionStatus"]["code"] or "Preliminary" == course["sectionStatus"]["code"])):
                    courseJSON = {
                        "@key": course["course"]["courseNumber"],
                        "@title": course["course"]["title"],
                        "@syllabusTerm": "",
                        "@originalCourseName": "",
                        "@courseDefinition": course["course"]["courseId"] # new course coding for the new courses website
                    }
                    # Grabs the necessary variables to build the syllabus URL
                    syllabusTerm, originalCourseName = hasSyllabus(
                        f"{dept} {str(courseJSON['@key'])}", syllabusInfo)
                    # Adds the variables to the dictionary
                    courseJSON["@syllabusTerm"] = str(syllabusTerm)
                    courseJSON["@originalCourseName"] = str(originalCourseName)
                    # Prevents duplicated courses
                    if (courseJSON not in dept_courses_array):
                        dept_courses_array.append(courseJSON)

            # Sort courses in a department
            for i in range(len(dept_courses_array)):
                for j in range(len(dept_courses_array)):
                    if (j < (len(dept_courses_array) - 1)):
                        if (courseOneIsHigher(dept_courses_array[j], dept_courses_array[j+1])):
                            dept_courses_array[j], dept_courses_array[j + 1] = dept_courses_array[j+1], dept_courses_array[j]
            # Adds the array of courses in that department to the courses dictionary
            courses.update({f"{dept}": dept_courses_array})

    # If there are courses in that session, add it to the set of courses
    if (len(courses) > 0):
        # Backup the courses for that session
        try:
            with open(f"static/data/backedUpSessions/{year}{term}.json", "w") as sessionData:
                json.dump({f"{year}{term}": courses}, sessionData, indent=4)

        except:
            print("Could not back up session data")

        courseJSONData['sessions'].update({f"{year}{term}": courses})

# W: winter, S: Summer
def updateData():
    # getData(str(year + 1), "W")
    # getData(str(year + 1), "S")
    getData(str(year), "W")
    getData(str(year), "S")
    getData(str(year - 1), "W")
    getData(str(year - 1), "S")

    try:
        with open("static/data/lfs-course-data.json", "r") as courseData:
            currentSavedJSONData = json.loads(courseData.read())
        # If current data is valid, then back it up (this happens before we update it)
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
            print(
                f'Finished reverting data at: {time.strftime("%A, %d. %B %Y %I:%M:%S %p")}')
            courseData.close()
        return

    # If data successfully backs up
    try:
        with open("static/data/lfs-course-data.json", "w") as courseData:
            json.dump(courseJSONData, courseData, indent=4)
            print(
                f'Data updated at: {time.strftime("%A, %d. %B %Y %I:%M:%S %p")}')
        courseData.close()
    except:
        print("Data failed to update. Reverting data update.")
        with open("static/data/lfs-course-data-backup.json", "r") as courseData:
            backedUpJSONData = json.loads(courseData.read())
            courseData.close()
        with open("static/data/lfs-course-data.json", "w") as courseData:
            json.dump(backedUpJSONData, courseData, indent=4)
            print(
                f'Finished reverting data at: {time.strftime("%A, %d. %B %Y %I:%M:%S %p")}')
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
