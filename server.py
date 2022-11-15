from flask import Flask, render_template
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


@app.route("/question/<question_id>")
def show_question(question_id):
    question = get_one_question(question_id)
    answers = get_answers(question_id)
    return render_template('base.html', question=question, answers=answers)


@app.route('/question/<question_id>/new-answer', methods=['POST'])
def post_answer():
    pass


if __name__ == "__main__":
    app.run(debug=True)
