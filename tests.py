from flask import Flask

from functions import update_terms_and_courses

app = Flask(__name__)

@app.cli.command("test_update_terms_and_courses")
def test_update_terms_and_courses():
    print("Test starts - update_terms_and_courses")
    update_terms_and_courses()
