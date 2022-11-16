import data_handler
import time

ANSWERS_DATA = 'sample_data/answer.csv'
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

def add_answer(message, question_id):
    id = data_handler.generate_id(data_handler.get_all_answers())
    record = {
        'id': id,
        'submission_time': int(time.time()),
        'vote_number': 0,
        'question_id': question_id,
        'message': message,
        'image': ''
    }

    data_handler.append_to_csv(record, ANSWERS_DATA)

def answer_vote(answer_id, vote):
    answers = data_handler.get_all_answers()
    for i, answer in enumerate(answers):
        if answer['id'] == answer_id:
            question_id = answer['question_id']
            vote_number = int(answers[i]['vote_number'])
            vote_number += vote
            answers[i]['vote_number'] = vote_number

    data_handler.overwrite_csv(answers, ANSWER_HEADER, ANSWERS_DATA)

    return question_id