import data_handler
import time

QUESTIONS_DATA = 'sample_data/question.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']

def add_question(question, files):
    id = data_handler.generate_id(data_handler.get_all_questions())
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