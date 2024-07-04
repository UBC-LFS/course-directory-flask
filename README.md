# LFS Course Directory with Flask
This project displays the courses available in the selected session alongside the most recent available syllabus.

### 0. Clone the repository
```
git clone https://github.com/UBC-LFS/course-directory-flask.git
```

### 1. Install apache2 and mod-wsgi
```
$ sudo apt-get install apache2 libapache2-mod-wsgi-py3
```

After that, you need to configure required settings in apache2

### 2. Add envirnnment variables to apache2's envvars
```
export COURSE_DIR_API_URL="URL"
export COURSE_DIR_API_EXP_URL="URL-ACADEMIC"
export COURSE_DIR_CLIENT_ID=""
export COURSE_DIR_CLIENT_SECRET=""
export COURSE_DIR_MODE="prod"
```

### 3. Install requirement pakcages
```
$ sudo apt install python3-venv
$ python3 -m venv venv
$ source venv/bin/activate (Windows: venv\Scripts\activate)
$ pip3 install -r requirements.txt
```

### 4. IMPORTANT: Add **syllabi** information
All the syllabi folders should be stored in the `templates/syllabi` folder.

### 4. Rename a **public_example** to **public**

### 5. How to run
```
$ python main.py
```
And then go to http://127.0.0.1:5000/


Thank you.