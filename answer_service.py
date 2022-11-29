import data_handler
import time

ANSWERS_DATA = 'answer'
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'user', 'message', 'image']


def get_answers():
    return data_handler.read_from_table(ANSWERS_DATA)


def get_answers_to_question(question_id):
    answers = get_answers()
    return [answer for answer in answers if answer['question_id'] == question_id]


def add_answer(answer, question_id, files):
    id = data_handler.generate_id(get_answers())
    record = {
        'id': id,
        'submission_time': int(time.time()),
        'vote_number': 0,
        'question_id': question_id,
        'user': answer['user'],
        'message': answer['message'],
        'image': ''
    }

    if files['image'].filename != '':
        record['image'] = f'answer_{id}.png'
        data_handler.save_image(files['image'], f'answer_{id}.png')

    data_handler.append_to_csv(record, ANSWERS_DATA)


def delete_answer(answer_id):
    answers = get_answers()
    for i, answer in enumerate(answers):
        if answer['id'] == answer_id:
            if answer['image'] != '':
                data_handler.delete_image(answer['image'])
            answers.pop(i)

    data_handler.overwrite_csv(answers, ANSWER_HEADER, ANSWERS_DATA)


def delete_answers_with_question(question_id):
    deleted_answers = get_answers_to_question(question_id)

    for answer in deleted_answers:
        delete_answer(answer['id'])


def answer_vote(answer_id, vote):
    answers = get_answers()
    for i, answer in enumerate(answers):
        if answer['id'] == answer_id:
            question_id = answer['question_id']
            answers[i]['vote_number'] += vote

    data_handler.overwrite_csv(answers, ANSWER_HEADER, ANSWERS_DATA)

    return question_id
