from flask import Flask, render_template, send_from_directory
import json
from get_course_data import updateData, getCoursesWithSyllabus
import os
import requests

app = Flask(__name__)

@app.route("/")
def home():
    # Updating data takes around 3 seconds, since the data does not change that often, we could make it update data daily or weekly?
    # updateData() 
    with open("static/data/lfs-course-data.json", "r") as courseData:
        courseJSONData = json.loads(courseData.read())["sessions"]
    courseData.close()
    return render_template("index.html", courseJSONData = courseJSONData)

# Opens the syllabus URL
@app.route("/coursedirectory/<session>/<course>/")
def courseDirectory(session, course):
    return render_template(f"CourseDirectory/{session}/{course}/index.html")

# If the syllabus has a link that redirects to a PDF file
@app.route("/coursedirectory/<session>/<course>/<source>/<file>/")
def courseDirectorySource(session, course, source, file):
    return send_from_directory("templates", f"CourseDirectory/{session}/{course}/{source}/{file}")

if __name__ == "__main__":
    app.run(debug=True)
