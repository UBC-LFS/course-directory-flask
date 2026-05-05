import os
import re
import json
import requests
from slugify import slugify
from datetime import date
from utils import *


def get_data(url, path, params):
    basic_url = os.environ.get(url) + path + '?pageSize=500' + params
    data = []
    has_next_page = 'true'
    offset_token = None
    while has_next_page == 'true':
        link = basic_url
        if offset_token:
            link += '&offsetToken=' + offset_token
        
        res = requests.get(link, headers = {
                'x-client-id': os.environ['COURSE_DIR_CLIENT_ID'], 
                'x-client-secret': os.environ['COURSE_DIR_CLIENT_SECRET']
            }
        )

        if res.status_code == 200:
            data.extend(res.json()['pageItems'])
            has_next_page = res.headers['x-next-page']
            if has_next_page == 'true':
                offset_token = res.headers['x-offset-token']
        else:
            print('Failed to get data via API for some reason.')
            break
    
    return data


def makeYearCode(year):
    yaerCodes = []
    for y in [year, year-1, year-2]:
        next_year = str(y+1)[2:]
        yaerCodes.append(f'{y}-{next_year}_UBC-V')
    
    return yaerCodes


def get_terms():
    year, _ = get_date_info()
    yearCodes = makeYearCode(year)
    
    data = []
    for yearCode in yearCodes:
        terms = get_data('COURSE_DIR_API_URL', ACADEMIC_PERIODS, '&academicYearCode=' + yearCode)
        for term in terms:
            if str(year) in term['academicPeriod']['academicPeriodName'] or str(year - 1) in term['academicPeriod']['academicPeriodName']:
                data.append(term['academicPeriod']['academicPeriodName'])
    
    data.sort(reverse=True)
    return data


def get_courses():
    terms = get_terms()
    syllabi = get_syllabi()

    valid_terms = []
    courses_data = {}
    for term in terms:
        print('\nTerm:', term)
        for subject in SUBJECTS:
            params = '&academicPeriodName={0}&courseSubject={1}&courseSectionStatus={2}'.format(term, subject, 'Open')
            courses = get_data('COURSE_DIR_API_EXP_URL', COURSE_DETAILS, params)
            
            print('Checking...', subject, len(courses))
            
            if len(courses) > 0:
                for course in courses:
                    term = course['academicPeriod']['academicPeriodName']

                    name = '{0} {1} {2}'.format(subject, course['course']['courseNumber'], course['sectionNumber'])
                    syllabus_key = name.replace(' ', '_')
                    has_syllabus = False
                    syllabus = { 'term': '', 'course_code': '' }
                    if syllabus_key in syllabi.keys():
                        syllabus_value = syllabi[syllabus_key].split('|')
                        has_syllabus = True
                        syllabus['term'] = syllabus_value[0]
                        syllabus['course_code'] = syllabus_value[1]

                    instructional_format = course['instructionalFormat']['code']
                    temp_course = '{0} {1}'.format(subject, course['course']['courseNumber'])

                    if instructional_format in VALID_TYPES or temp_course in EXCEPTION_COURSES:
                        title = remove_prepositions(course['course']['title'])
                        section_number = course['sectionNumber']
                        title_sec = '{}-{}-sec-{}'.format(title, course['academicPeriod']['academicPeriodName'][:4], section_number)
                        slug = '{0}/{1}'.format(slugify(title), slugify(title_sec))

                        item = {
                            'name': '{0} {1} {2}'.format(subject, course['course']['courseNumber'], section_number),
                            'title': title,
                            'instructional_format': instructional_format,
                            'has_syllabus': has_syllabus,
                            'syllabus': syllabus,
                            'status': course['courseSectionStatus']['code'],
                            'slug': slug
                        }
                        
                        if term in courses_data.keys():
                            courses_data[term]['list'].append(item)
                        else:
                            courses_data[term] = {
                                'list': [],
                                'by_subject': {}
                            }

                        if subject in courses_data[term]['by_subject'].keys():
                            courses_data[term]['by_subject'][subject].append(item)
                        else:
                            courses_data[term]['by_subject'][subject] = []

        if term in courses_data.keys() and len(courses_data[term]['list']) > 0:
            valid_terms.append(term)
            print('{0} valid courses found.'.format(len(courses_data[term]['list'])))
        else:
            print('No valid courses found in this term -', term)

    for k, v in courses_data.items():
        v['list'].sort(key=lambda d: d['name'])

        for a, b in v['by_subject'].items():
            b.sort(key=lambda d: d['name'])
    

    sorted_terms = sorted(enumerate(valid_terms), key=lambda x: (-extract_year_info(x[1])[0], -extract_year_info(x[1])[1], get_priority(x[1]), x[0]))

    avail_terms = [item for _, item in sorted_terms]

    print('\nAvailable terms:', avail_terms)
    data = {
        'terms': avail_terms, 
        'courses': courses_data
    }

    # Save as json
    with open(os.path.join(PUBLIC_FOLDER_PATH, 'data.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    return data

    
def load_terms_and_courses():
    year, target = get_date_info()

    data = {}
    data_file = os.path.join(PUBLIC_FOLDER_PATH, 'data.json')
    if os.path.isfile(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
    else:
        data = get_courses()
    
    return data, year, target


def update_terms_and_courses():
    get_courses()
    print('Done: update terms and courses')


def get_syllabi():
    syllabi = {}

    syllabi_path = os.path.join(BASE_URL, 'templates', 'syllabi')
    if os.path.exists(syllabi_path):
        dirs = os.listdir(syllabi_path)
        dirs.sort(reverse=True)
        for dir in dirs:
            dir_path = os.path.join(syllabi_path, dir)
            if os.path.isdir(dir_path):
                syllabus_course_names = os.listdir(dir_path)
                for course_name in syllabus_course_names:
                    course_name_sp = course_name.split(' ')
                    if len(course_name_sp) > 2:
                        key = '{0}_{1}_{2}'.format(course_name_sp[0], course_name_sp[1], course_name_sp[2])
                        if key not in syllabi.keys():
                            syllabi[key] = '{0}|{1}'.format(dir, course_name)

    return syllabi


# Helper functions

def get_date_info():
    year = date.today().year
    month = date.today().month

    target = None
    if 1 <= month <= 4:
        year -= 1
        target = 'Winter Term 2'
    elif 5 <= month <= 8:
        target = 'Summer'
    elif 9 <= month <= 12:
        target = 'Winter Term 1'
    
    return year, target


def remove_prepositions(text):
    preps = ['in', 'on', 'at', 'by', 'with', 'for', 'about', 'to']
    pattern = r'\b(' + '|'.join(preps) + r')\b\s*'
    return re.sub(pattern, '', text, flags=re.IGNORECASE)


def extract_year_info(s):
    first = s.split()[0]
    
    if '-' in first:
        start_year = int(first.split('-')[0])
        return (start_year, 1)
    else:
        return (int(first), 0)


def get_priority(s):
    priority = {'Session': 1, 'Term 1': 2, 'Term 2': 3}
    for key in priority:
        if key in s:
            return priority[key]
    return float('inf')