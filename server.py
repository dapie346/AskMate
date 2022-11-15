from flask import Flask, render_template
import data_handler
from data_handler import *

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def home_page():
    all_questions = get_all_user_story()
    all_questions = sorted(all_questions, key=lambda d: d['submission_time'])

    return render_template('home_page.html', all_questions=all_questions)

@app.route("/add-question")
def add_question():
    return render_template('add-question.html')

if __name__ == "__main__":
    app.run(debug=True)
