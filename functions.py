import os
import json
import requests
from datetime import date
from slugify import slugify
from dotenv import load_dotenv
from utils import *

load_dotenv()


def get_data(url, path, params):
    data = []
    has_next_page = 'true'
    page = 1
    while has_next_page == 'true':
        res = requests.get(
            os.getenv(url) + path + '?pageSize=500&page=' + str(page) + params,
            headers = {
                'x-client-id': os.getenv('Client_ID'), 
                'x-client-secret': os.getenv('Client_Secret')
            }
        )

        if res.status_code == 200:
            data.extend(res.json()['pageItems'])

            has_next_page = res.headers['x-next-page']
            page += 1
        else:
            print('Failed to get data via API for some reason.')
            break
    
    return data


def get_terms(year, items):
    terms = {}
    for item in items:
        if ('UBC-V' in item['academicPeriod']['academicPeriodName']) and (str(year) in item['academicPeriod']['academicPeriodName'] or str(year - 1) in item['academicPeriod']['academicPeriodName']):
            terms[ item['academicPeriod']['academicPeriodId'] ] = item['academicPeriod']['academicPeriodName']
            
    # Save as json
    with open(os.path.join(os.getcwd(), 'public', str(year) + '_' + ACADEMIC_PERIODS + '.json'), 'w', encoding='utf-8') as f:
        json.dump(terms, f)

    return terms


def get_courses(this_year, terms):
    data = {}

    term_temp = []
    term_names = {}
    courses = {}
    term_map = {}
    for year in [this_year, this_year - 1]:
        if str(year) not in term_names.keys():
            term_names[str(year)] = []

        for subject in SUBJECTS:
            course_items = get_data('API_EXP_URL', COURSE_DETAILS, '&academicYear=' + str(year) + '&courseSubject=' + subject)
            print('Reading =====> ' + subject, year, len(course_items))
            if len(course_items) > 0:
                for item in course_items:
                    term_id = item['academicPeriod']['academicPeriodId']
                    term_name = terms[term_id]

                    if term_id not in term_temp:
                        term_names[str(year)].append({ 'id': term_id, 'name': term_name, 'slug': slugify(term_name) })
                        term_temp.append(term_id)
                    
                    if term_id not in term_map.keys():
                        term_map[slugify(term_name)] = term_id

                    name = '{0} {1} {2}'.format(subject, item['course']['courseNumber'], item['sectionNumber'])
                    data = {
                        'name': name,
                        'title': item['course']['title'],
                        'slug': slugify(name),
                        'section_status': item['sectionStatus']
                    }
                    
                    if term_id not in courses.keys():
                        courses[term_id] = { 
                            'list': [],
                            'by_subject': {},
                            'slug': slugify(term_name)
                        }
                    courses[term_id]['list'].append(data)

                    if subject not in courses[term_id]['by_subject'].keys():
                        courses[term_id]['by_subject'][subject] = []
                    courses[term_id]['by_subject'][subject].append(data)
    
    curr_year_terms = term_names[str(this_year)]
    prev_year_terms = term_names[str(this_year-1)]

    curr_year_terms.sort(key=lambda l: l['name'])
    prev_year_terms.sort(key=lambda l: l['name'])

    curr_year_terms.extend(prev_year_terms)

    for k, v in courses.items():
        v['list'].sort(key=lambda d: d['name'])
        for a, b in v['by_subject'].items():
            b.sort(key=lambda d: d['name'])
        

    data = { 'term_map': term_map, 'terms': curr_year_terms, 'courses': courses }

    # Save as json
    with open(os.path.join(os.getcwd(), 'public', str(this_year) + '_' + COURSE_DETAILS + '.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f)

    return data


def load_terms_courses():
    print('load_terms_courses ==========')
    year, _ = get_date_info()

    terms = []
    courses = {}

    academic_periods_file = os.path.join(os.getcwd(), 'public', str(year) + '_' + ACADEMIC_PERIODS + '.json')
    course_details_file = os.path.join(os.getcwd(), 'public', str(year) + '_' + COURSE_DETAILS + '.json')

    if os.path.isfile(academic_periods_file):
        with open(academic_periods_file, 'r', encoding='utf-8') as f:
            terms = json.loads(f.read())
    else:
        term_items = get_data('API_URL', ACADEMIC_PERIODS, '')
        terms = get_terms(year, term_items)

    if os.path.isfile(course_details_file):
        with open(course_details_file, 'r', encoding='utf-8') as f:
            courses = json.loads(f.read())
    else:
        courses = get_courses(year, terms)
    
    return courses


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