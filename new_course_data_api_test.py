from datetime import date
import time
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Loads API tokens
clientID = os.getenv("CLIENT-ID")
clientSecret = os.getenv("CLIENT-SECRET")

courseJSONData = {"sessions": {}}
year = date.today().year

LFSDepts = ['APBI', 'FNH', 'FOOD', 'FRE', 'GRS', 'HUNU', 'LFS', 'LWS', 'PLNT', 'SOIL']

# Has Syllabus function

def getData(year, term):
    courses = {}
    # Run getCoursesWithSyllabus
    for dept in LFSDepts:
        url = f"https://stg.api.ubc.ca/academic-exp/v1/course-section-details?academicYear={year}&courseSubject={dept}_V&page=1&pageSize=500"
        data = requests.get(url, headers={"x-client-id":clientID, "x-client-secret":clientSecret}).text
        courseData = json.loads(data)['pageItems']
        # if (len(courseData) > 0):
        #     print(year + term)
        #     # print(courseData)
        #     break

        for course in courseData:
            # if  course["academicPeriod"]["academicPeriodName"] is term
            # 'academicPeriodName': '2023-24 Winter Term 2 (UBC-V)'}
            if (term == course["academicPeriod"]["academicPeriodName"].split(" ")[1][0]):
                courseJSON = {
                    "@key": course["course"]["courseNumber"],
                    "@title": course["course"]["title"],
                    "@syllabusTerm": year + term,
                    "@originalCourseName": "" # get from syllabus
                }
                # dept_courses_array.append(courseJSON)
                print(course["academicPeriod"]["academicPeriodName"] + "  " + term)
                
        # courses.update({f"{dept}":dept_courses_array})

    courseJSONData['sessions'].update({f"{year}{term}":courses})


def updateData():
    getData(str(year + 1), "W")
    getData(str(year + 1), "S")
    getData(str(year), "W")
    getData(str(year), "S")
    getData(str(year - 1), "W")
    getData(str(year - 1), "S")

updateData()