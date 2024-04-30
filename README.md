# **LFS Course Directory (with Flask)**
This project displays the courses available in the selected session alongside the most recent available syllabus.

# **Notes for maintaining this project:**
Last updated: 2024-04-30

## **Updating the syllabuses**
When adding new syllabuses, ensure that the points below remain consistent. Not doing so may result in syllabuses not properly displaying:
1. All syllabuses are stored in the `templates/CourseDirectory` folder.
2. Each subfolder in `templates/CourseDirectory` is named based on the session name (e.g., `2022W1`).
3. Within the session folder, there should be another subfolder named after the course.
4. Inside the course folder, there should be an `index.html` file and maybe a `source` folder containing the syllabus if the syllabus is not the `index.html` file.

## **Notes for developers**
### **Clone the repository**
```
git clone https://github.com/UBC-LFS/course-directory-flask.git
```
### **Setting up**
``` python
pip install virtualenv
virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
```

`.env`
```
CLIENT-ID = 
CLIENT-SECRET = 
COURSES-URL = 
```

1. Create an empty folder called "CourseDirectory" inside the "templates" folder if it doesn't already exist.

2. Upload course syllabuses to the "CourseDirectory" folder.

### **Running the web app**
Run:
```
main.py
```
Go to: http://127.0.0.1:5000/ (localhost)

### **What does each file do?**
#### **Python code:**
- **main.py**
  - The web server
  - Render web pages
  - Contains the code for automatically fetching and updating the course data every day.

- **get_course_data.py**
  - Fetches course data and creates a JSON file for it
  - Finds out what courses have a syllabus
  - Automatically creates backup files for the courses in each session (`static/data/backedUpSessions`)
  - Automatically backs up `lfs-course-data.json` before attempting to update it
    - If the backup fails, stops trying to retrieve new data (will not update unless we can create a backup file).

#### **Templates (Contains all HTML files and syllabuses)**
- **index.html** (Home page)
  - Contains JavaScript code for retrieving the course data from Flask when the page renders
  - Builds a table with course data
  - Code for search bar and syllabus toggle

- **404.html** (404 page)
- **error.html** (Error page)
- **footer and navigationbar .html**
  - The navigation bar and footer displayed on all pages
- **CourseDirectory** (contains all syllabuses)

#### **Static (Contains all JS, CSS, images, and data)**
- **JavaScript**
  - dropdownMenu.js
    - Code to create the dropdown menus
  - displayCourses.js
    - Code to create the pagination
- **CSS**
  - main.css (styles for index.html)
  - 404.css (styles for 404 and error .html)
  - navandfooter.css (styles for footer and navigationbar .html)
- **Images** (all images used on the website)
- **Data**
    - lfs-course-data.json (course info retrieved every day)
    - lfs-course-data-backup.json (backed-up version of lfs-course-data.json; backed up daily)
    - backedUpSessions
        - Backed-up course info for each session
        - Not for the web app

### **Potential future error(s)**
- All data for courses are retrieved from an API. If this API changes the way the data is formatted, the functions to retrieve and format the data may stop working.
  - If this happens and new data cannot be retrieved, this app will stop updating the JSON file. However, if the JSON file updates and results in an error, there is a backup file that will be used instead.
- Course URL may change. Parameters for this new web page may also change -> will need to update the URL in `.env` + the parameters in `index.html` line 145