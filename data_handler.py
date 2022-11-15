import csv
import time
import random

QUESTIONS_DATA = 'sample_data/question.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWERS_DATA = 'sample_data/answer.csv'


def get_all_questions():
    with open('sample_data/question.csv', 'r') as f:
        dict_reader = csv.DictReader(f)
        list_of_dict = list(dict_reader)
    return list_of_dict


def generate_id(csv_data):
    while True:
        id = random.randint(1,9999)
        if not any(id == record['id'] for record in csv_data):
            return id


def write_question(question):
    id = generate_id(get_all_questions())
    record = {
        'id': id,
        'submission_time': int(time.time()),
        'view_number': 0,
        'vote_number': 0,
        'title': question['title'],
        'message': question['message'],
        'image': '', # add image here
    }
    with open(QUESTIONS_DATA, "a") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(record.values())
        file.close()

    return id


def get_one_question(question_id):
    with open(QUESTIONS_DATA) as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            if row['id'] == question_id:
                return row


def get_answers_to_question(question_id):
    answers = []
    with open(ANSWERS_DATA) as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            if row['question_id'] == question_id:
                answers.append(row)
    return answers


def get_all_answers():
    with open(ANSWERS_DATA) as f:
        dict_reader = csv.DictReader(f)
        list_of_dict = list(dict_reader)
    return list_of_dict


def write_answer(message, question_id):
    id = generate_id(get_all_answers())
    record = {
        'id': id,
        'submission_time': int(time.time()),
        'vote_number': 0,
        'question_id': question_id,
        'message': message,
        'image': '',  # add image here
    }
    with open(ANSWERS_DATA, "a") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(record.values())
