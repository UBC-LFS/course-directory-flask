from flask import Flask, render_template, send_from_directory, redirect, url_for
import json
from get_course_data import updateData
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

def updateDataFunc():
    try:
        print("Attempting to update data")
        updateData()
    except:
        print(f'Unable to update data: {time.strftime("%A, %d. %B %Y %I:%M:%S %p")}')

# Update data when app runs (incase there are new syllabuses added)
updateDataFunc()

app = Flask(__name__)

@app.route("/")
def home():
    try:
        with open("static/data/lfs-course-data.json", "r") as courseData:
            courseJSONData = json.loads(courseData.read())["sessions"]
        courseData.close()
        return render_template("index.html", courseJSONData = courseJSONData)
    
    # Use backed up data
    except:
        try:
            with open("static/data/lfs-course-data-backup.json", "r") as courseData:
                courseJSONData = json.loads(courseData.read())["sessions"]
            courseData.close()
            return render_template("index.html", courseJSONData = courseJSONData)
        # If even the backed up data fails
        except:
            return redirect(url_for('error'))

# Opens the syllabus URL
@app.route("/coursedirectory/<session>/<course>/")
def courseDirectory(session, course):
    try:
        return render_template(f"CourseDirectory/{session}/{course}/index.html")
    except:
        return redirect(url_for('error'))

# If the syllabus has a link that redirects to a PDF file
@app.route("/coursedirectory/<session>/<course>/<source>/<file>/")
def courseDirectorySource(session, course, source, file):
    try:
        return send_from_directory("templates", f"CourseDirectory/{session}/{course}/{source}/{file}")
    except:
        return redirect(url_for('error'))

# 404 Page
@app.route("/error")
def error():
  return render_template('error.html')

# 404 Page
@app.errorhandler(404)
def page_not_found(e):
  try:
    return render_template('404.html')
  except:
      return redirect(url_for('error'))

def updateDataOrNo():
    # If it's 4 am, update the data
    if (str(time.strftime("%I %p")) == str("04 AM")):
        updateDataFunc()

# Create the background scheduler
scheduler = BackgroundScheduler()
# Create the job and run updateDataOrNo() every hour
scheduler.add_job(func=updateDataOrNo, trigger="interval", minutes=60)
# Start the scheduler
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    app.run(debug=True)
