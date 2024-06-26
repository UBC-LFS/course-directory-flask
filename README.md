# LFS Course Directory with Flask
This project displays the courses available in the selected session alongside the most recent available syllabus.

### 0. Clone the repository
```
git clone https://github.com/UBC-LFS/course-directory-flask.git
```

### 1. Install requirement pakcages
```
$ sudo apt install python3-venv
$ python3 -m venv venv
$ source venv/bin/activate (Windows: venv\Scripts\activate)
$ pip3 install -r requirements.txt
```

### 2. Make a `.env` file
```
API_URL = "URL"
API_EXP_URL = "URL-ACADEMIC"

Client_ID = ""
Client_Secret = ""
```

### 3. IMPORTANT: Add **syllabi** information
All the syllabi folders should be stored in the `templates/syllabi` folder.

### 4. Rename a **public_example** to **public**

### 5. How to run
```
$ python main.py
```
And then go to http://127.0.0.1:5000/


Thank you.