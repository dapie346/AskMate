from flask import Flask, render_template, request, redirect, url_for
from data_handler import *
from util import *
import question_controller
import data_handler

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def home_page():
    order_by = request.args.get('order_by', default='submission_time')
    order_direction = request.args.get('order_direction', default='desc')
    all_questions = sort_records(get_all_questions(), order_by, order_direction)
    return render_template('home_page.html', all_questions=all_questions)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        id = question_controller.add_question(request.form, request.files)
        return redirect(url_for('show_question', question_id=id))
    return render_template('add-question.html')

@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    question = get_one_question(question_id)
    if request.method == 'POST':
        question_controller.update_question(question_id, request.form['title'], request.form['message'])
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('edit-question.html', title=question['title'], message=question['message'])

@app.route("/question/<question_id>")
def show_question(question_id):
    question = get_one_question(question_id)
    answers = get_answers_to_question(question_id)
    question_controller.count_views(question_id)
    answers = sorted(answers, key=lambda d: d['vote_number'], reverse=True)
    return render_template('display-question.html', question=question, answers=answers)

@app.route("/question/<question_id>/vote-up")
def question_upvote(question_id):
    question_controller.question_vote(question_id, 1)
    return redirect(url_for('home_page'))

@app.route("/question/<question_id>/vote-down")
def question_downvote(question_id):
    question_controller.question_vote(question_id, -1)
    return redirect(url_for('home_page'))

@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'POST':
        message = request.form['message']
        write_answer(message, question_id)
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('post_answer.html')


@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'POST':
        question_controller.delete_question(question_id)
    return redirect('/')

@app.route("/answer/<answer_id>/vote-up")
def answer_upvote(answer_id):
    question_id = answer_vote(answer_id, 1)
    return redirect(url_for('show_question', question_id=question_id))

@app.route("/answer/<answer_id>/vote-down")
def answer_downvote(answer_id):
    question_id = answer_vote(answer_id, -1)
    return redirect(url_for('show_question', question_id=question_id))

@app.route("/answer/<answer_id>/delete", methods=['GET', 'POST'])
def delete_answer(answer_id):
    if request.method == 'POST':
        data_handler.delete_answer(answer_id)
    return redirect(url_for('show_question', question_id=request.form.get("open")))


if __name__ == "__main__":
    app.run(debug=True)
