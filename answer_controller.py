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