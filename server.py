from flask import Flask, render_template, request, redirect, url_for

import tag_service
import question_service
import answer_service
import comment_service
from data_handler import *

app = Flask(__name__)


@app.route("/")
def home_page():
    order_by = request.args.get('order_by', default='submission_time')
    order_direction = request.args.get('order_direction', default='desc')
    all_questions = question_service.get_questions(order_by, order_direction+' limit 5')
    return render_template('home_page.html', all_questions=all_questions, page='home_page')


@app.route("/list")
def home_page_list():
    order_by = request.args.get('order_by', default='submission_time')
    order_direction = request.args.get('order_direction', default='desc')
    all_questions = question_service.get_questions(order_by, order_direction)
    return render_template('home_page.html', all_questions=all_questions, page='home_page_list')


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        id = question_service.add_question(request.form, request.files)
        return redirect(url_for('show_question', question_id=id))
    return render_template('add-question.html')


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    question = question_service.get_question(question_id)
    if request.method == 'POST':
        question_service.update_question(question_id, request.form['title'], request.form['message'])
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('edit-question.html', title=question['title'], message=question['message'])


@app.route("/question/<question_id>")
def show_question(question_id):
    question_service.count_views(question_id)
    question = question_service.get_question(question_id)
    answers = answer_service.get_answers_to_question(question_id)
    comments = comment_service.get_comments_to_question(question_id)
    tags = tag_service.get_question_tags(question_id)
    return render_template('display-question.html', question=question, answers=answers, tags=tags, comments=comments)


@app.route("/question/<question_id>/vote-up")
def question_upvote(question_id):
    question_service.question_vote(question_id, 1)
    return redirect(url_for('home_page'))


@app.route("/question/<question_id>/vote-down")
def question_downvote(question_id):
    question_service.question_vote(question_id, -1)
    return redirect(url_for('home_page'))


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'POST':
        answer_service.add_answer(request.form, question_id, request.files)
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('post_answer.html')


@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    question_service.delete_question(question_id)
    return redirect(url_for('home_page'))


@app.route("/question/<question_id>/new-tag", methods=['GET', 'POST'])
def tag_question(question_id):
    tags = tag_service.get_tags()
    question_tags = tag_service.get_question_tags(question_id)
    if request.method == 'POST':
        if 'select_tag' in request.form:
            tag_id = request.form['tag_id']
        elif 'add_tag' in request.form:
            tag_id = tag_service.add_tag(request.form['tag'])
        question_service.tag_question(question_id, tag_id)
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('tag_question.html', tags=tags, question_tags=tag_service.get_tag_names_from_list(question_tags))


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def remove_tag(question_id, tag_id):
    tag_service.remove_tag(question_id, tag_id)
    return redirect(url_for('show_question', question_id=question_id))


@app.route("/answer/<answer_id>/vote-up")
def answer_upvote(answer_id):
    question_id = answer_service.answer_vote(answer_id, 1)
    return redirect(url_for('show_question', question_id=question_id))


@app.route("/answer/<answer_id>/vote-down")
def answer_downvote(answer_id):
    question_id = answer_service.answer_vote(answer_id, -1)
    return redirect(url_for('show_question', question_id=question_id))


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    question_id = answer_service.delete_answer(answer_id)
    return redirect(url_for('show_question', question_id=question_id))


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def new_comment_to_question(question_id):
    if request.method == 'POST':
        comment_service.add_to_question(request.form['message'], question_id)
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('new-comment.html')


@app.route("/question/<question_id>/<answer_id>/new-comment", methods=['GET', 'POST'])
def new_comment_to_answer(answer_id, question_id):
    if request.method == 'POST':
        comment_service.add_to_answer(request.form['message'], question_id, answer_id)
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('new-comment.html')


@app.route("/comments/<comment_id>/delete", methods=['GET', 'POST'])
def delete_comment(comment_id):
    comment = comment_service.get_comment(comment_id)
    comment_service.delete_comment(comment)
    return redirect(url_for('show_question', question_id=comment['question_id']))


@app.route("/comments/<comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment = comment_service.get_comment(comment_id)
    if request.method == 'POST':
        comment_service.edit_comment(comment, request.form['message'])
        return redirect(url_for('show_question', question_id=comment['question_id']))
    return render_template('edit-comment.html', message=comment['message'])


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = answer_service.get_answer(answer_id)
    if request.method == 'POST':
        question_id = answer_service.update_answer(answer_id, request.form['message'])
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('edit_answer.html', message=answer['message'])


def duplicate_handler_for_search(q_list, a_list):
    for i in a_list:
        if i not in q_list:
            q_list.append(i)
    return q_list


@app.route("/search/<word>", methods=['POST'])
def basic_search(word):
    search_phrase = request.form.get('search')
    if request.method == 'POST':
        search_data = search_for(search_phrase)
        answer_data = search_for_answer(search_phrase)
        results = duplicate_handler_for_search(search_data, answer_data)
        all_questions = read_from_table('question')
        return render_template('home_page.html', search_data=results, all_questions=all_questions,search_phrase=search_phrase)


if __name__ == "__main__":
    app.run(debug=True)
