from csv import DictReader
import csv
import time
import random

QUESTIONS_DATA = 'sample_data/question.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWERS_DATA = 'sample_data/answer.csv'


def get_all_questions():
    with open('sample_data/question.csv', 'r') as f:
        dict_reader = DictReader(f)

        list_of_dict = list(dict_reader)

    return list_of_dict

def generate_question_id():
    questions = get_all_questions()
    while True:
        id = random.randint(1,9999)
        if not any(id == question['id'] for question in questions):
            return id

def write_question(question):
    id = generate_question_id()
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
        csv_file = DictReader(file)
        for row in csv_file:
            if row['id'] == question_id:
                return row

def get_answers(question_id):
    answers = []
    with open(ANSWERS_DATA) as file:
        csv_file = DictReader(file)
        for row in csv_file:
            if row['question_id'] == question_id:
                answers.append(row)
    return answers
