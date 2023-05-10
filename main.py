from flask import Flask, render_template
import json
from get_course_data import updateData

app = Flask(__name__)

@app.route("/")
def home():
    # Updating data takes around 3 seconds, since the data does not change that often, we could make it update data daily or weekly?
    # updateData() 

    with open("static/data/lfs-course-data.json", "r") as courseData:
        courseJSONData = json.loads(courseData.read())["sessions"]
    courseData.close()
    return render_template("index.html", courseJSONData = courseJSONData)

if __name__ == "__main__":
    app.run(debug=True)
