from flask import Flask, render_template, request, abort, send_from_directory 
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from functions import *
from utils import *

app = Flask(__name__)


@app.route('/')
def home():
    select_term = request.args.get('term', None)
    select_subject = request.args.get('subject', None)
    select_syllabus = request.args.get('syllabus', None)

    data, year, target = load_terms_and_courses()
    if not target:
        abort(500)

    if request.base_url == request.url:
        for term in data['terms']:
            if str(year) in term['name'] and target in term['name']:
                select_term = term['slug']
                break
        select_subject = 'All'
    else:
        if not select_term or not select_subject:
            abort(404)
        if select_syllabus and (select_syllabus != 'on'):
            abort(404)
    
    if select_term not in data['term_map'].keys() or select_subject not in ['All'] + SUBJECTS:
        abort(404)

    term_id = data['term_map'][select_term]

    courses = []
    if term_id in data['courses'].keys():
        if select_subject == 'All':
            courses = data['courses'][term_id]['list']
        elif select_subject in SUBJECTS and select_subject in data['courses'][term_id]['by_subject'].keys():
            courses = data['courses'][term_id]['by_subject'][select_subject]

    if select_syllabus == 'on':
        temp_courses = []
        for course in courses:
            if course['has_syllabus']:
                temp_courses.append(course)
        courses = temp_courses
    
    return render_template('home.html', terms=data['terms'], courses=courses, selected_term=select_term, subjects=['All'] + SUBJECTS, selected_subject=select_subject, select_syllabus=select_syllabus, course_schedule_url=COURSE_SCHEDULE_URL)


@app.route('/syllabus/term/<term>/course/<course_code>/')
def get_syllabus(term, course_code):
    return render_template('syllabi/{0}/{1}/index.html'.format(term, course_code))


@app.route('/syllabus/term/<term>/course/<course_code>/source/<source_file>')
def get_file(term, course_code, source_file):
    return send_from_directory('templates', 'syllabi/{0}/{1}/source/{2}'.format(term, course_code, source_file))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', message=error), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', message=error), 500


# Scheduler: cron job - run everyday at 3AM
scheduler = BackgroundScheduler(timezone='America/Vancouver')
scheduler.add_job(update_terms_and_courses, 'cron', hour=3, minute=0)
scheduler.start()
atexit.register(lambda: scheduler.shutdown()) # Shut down the scheduler when exiting the app


if __name__ == '__main__':
    if os.environ['COURSE_DIR_MODE'] == 'prod':
        app.run(host='0.0.0.0')
    else:
        app.run(debug=True)