from flask import Flask, render_template, request, redirect
from data_handler import *

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def home_page():
    all_questions = get_all_questions()
    all_questions = sorted(all_questions, key=lambda d: d['submission_time'])

    return render_template('home_page.html', all_questions=all_questions)

@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        id = write_question(request.form)
        return redirect('/question/' + str(id))
    return render_template('add-question.html')

@app.route("/question/<question_id>")
def show_question(question_id):
    question = get_one_question(question_id)
    answers = get_answers(question_id)
    answers = sorted(answers, key=lambda d: d['vote_number'])
    return render_template('display-question.html', question=question, answers=answers)


if __name__ == "__main__":
    app.run(debug=True)
