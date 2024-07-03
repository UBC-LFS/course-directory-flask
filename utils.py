import os

BASE_URL = os.path.dirname(os.path.abspath(__file__))

PUBLIC_FOLDER_PATH = os.path.join(BASE_URL, 'public')
ACADEMIC_PERIODS = 'academic-periods'
COURSE_DETAILS = 'course-section-details'
SUBJECTS = ['AGEC_V', 'AANB_V', 'APBI_V', 'AQUA_V', 'FNH_V', 'FOOD_V', 'FRE_V', 'GRS_V', 'HUNU_V', 'LFS_V', 'LWS_V', 'PLNT_V', 'SOIL_V']

VALID_TYPES = ['Lecture', 'Research']
EXCEPTION_COURSES = ['FNH_V 326', 'FNH_V 426']

COURSE_SCHEDULE_URL = 'https://courses.students.ubc.ca/browse-courses/course/'