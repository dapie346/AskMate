import data_handler
import time

QUESTIONS_DATA = 'sample_data/question.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_questions():
    return data_handler.get_records(QUESTIONS_DATA)


def add_question(question, files):
    id = data_handler.generate_id(get_questions())
    record = {
        'id': id,
        'submission_time': int(time.time()),
        'view_number': 0,
        'vote_number': 0,
        'title': question['title'],
        'message': question['message'],
        'image': '',
    }
    if files['image'].filename != '':
        record['image'] = f'question_{id}.png'
        data_handler.save_image(files['image'], f'question_{id}.png')

    data_handler.append_to_csv(record, QUESTIONS_DATA)

    return id


def delete_question(question_id):
    questions = get_questions()
    for i, question in enumerate(questions):
        if question['id'] == question_id:
            if question['image'] != '':
                data_handler.delete_image(question['image'])
            questions.pop(i)

    data_handler.overwrite_csv(questions, QUESTION_HEADER, QUESTIONS_DATA)


def question_vote(question_id, vote):
    questions = get_questions()
    for i, question in enumerate(questions):
        if question['id'] == question_id:
            questions[i]['vote_number'] += vote

    data_handler.overwrite_csv(questions, QUESTION_HEADER, QUESTIONS_DATA)


def update_question(question_id, title, message):
    questions = get_questions()
    for i, question in enumerate(questions):
        if question['id'] == question_id:
            questions[i]['title'] = title
            questions[i]['message'] = message

    data_handler.overwrite_csv(questions, QUESTION_HEADER, QUESTIONS_DATA)


def count_views(question_id):
    questions = get_questions()
    for i, question in enumerate(questions):
        if question['id'] == question_id:
            question['view_number'] = question['view_number'] + 1

    data_handler.overwrite_csv(questions, QUESTION_HEADER, QUESTIONS_DATA)
