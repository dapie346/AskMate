from flask import Flask, render_template, request, redirect, url_for
from data_handler import *
from util import *

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
@app.route("/list", methods=['GET', 'POST'])
def home_page():
    order_by = request.args.get('order_by', default='submission_time')
    all_questions = sort_records(get_all_questions(), order_by)
    return render_template('home_page.html', all_questions=all_questions)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        print(request.files)
        if 'image' in request.files:
            file = request.files['image']
            filename = file.filename
            save_image(file, filename)
        else:
            filename = ''
        id = write_question(request.form, filename)
        return redirect(url_for('show_question', question_id=id))
    return render_template('add-question.html')


@app.route("/question/<question_id>")
def show_question(question_id):
    question = get_one_question(question_id)
    answers = get_answers_to_question(question_id)
    count_views(question_id)
    answers = sorted(answers, key=lambda d: d['vote_number'], reverse=True)
    return render_template('display-question.html', question=question, answers=answers)


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
        all_questions = get_all_questions()
        find_id(all_questions, question_id)
        save_all(all_questions)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
