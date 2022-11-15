from flask import Flask, render_template

from data_handler import *

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def home_page():
    all_questions = get_all_user_story()
    return render_template('base.html', all_questions=all_questions)


@app.route("/question/<question_id>")
def show_question(question_id):
    question = get_one_question(question_id)
    answers = get_answers(question_id)
    return render_template('base.html', question=question, answers=answers)


if __name__ == "__main__":
    app.run(debug=True)
