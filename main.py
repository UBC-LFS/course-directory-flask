import os
import json
from datetime import date
from flask import Flask, render_template, request, url_for, redirect, abort, send_from_directory 
from apscheduler.schedulers.background import BackgroundScheduler

import time
import atexit

from functions import *
from utils import *

app = Flask(__name__)



@app.route('/')
def home():    
    year, target = get_date_info()

    if not target:
        abort(500)

    select_term = request.args.get('term', None)
    select_subject = request.args.get('subject', None)

    data = load_terms_courses()

    if request.base_url == request.url:
        for term in data['terms']:
            if str(year) in term['name'] and target in term['name']:
                select_term = term['slug']
                break
        select_subject = 'All'
    else:
        if not select_term or not select_subject:
            abort(404)
    
    if select_term not in data['term_map'].keys() or select_subject not in ['All'] + SUBJECTS:
        abort(404)

    term_id = data['term_map'][select_term]

    courses = []
    if select_subject == 'All':
        courses = data['courses'][term_id]['list']
    elif select_subject in SUBJECTS:
        if select_subject in data['courses'][term_id]['by_subject'].keys():
            courses = data['courses'][term_id]['by_subject'][select_subject]
    
    return render_template('home.html', terms=data['terms'], courses=courses, selected_term=select_term, subjects=['All'] + SUBJECTS, selected_subject=select_subject)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', message=error), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', message=error), 500


def cron():
    print('Scheduling tasks running...')
    scheduler = BackgroundScheduler(timezone='America/Vancouver')
    # scheduler.add_job(load_terms_courses, 'cron', day=1, hour=6, minute=0)
    scheduler.add_job(load_terms_courses, 'cron', minute=13)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

# cron()

if __name__ == "__main__":
    app.run(debug=True)