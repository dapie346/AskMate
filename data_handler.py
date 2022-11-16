import os
from csv import DictReader
import csv
import time
import random

QUESTIONS_DATA = 'sample_data/question.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWERS_DATA = 'sample_data/answer.csv'
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

IMAGE_FOLDER = 'static/images'

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

def save_image(file, filename):
    file.save(os.path.join(IMAGE_FOLDER, filename))

def delete_image(filename):
    os.remove(os.path.join(IMAGE_FOLDER, filename))

def append_to_csv(row, filepath):
    with open(filepath, "a") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(row.values())

def overwrite_csv(data, headers, filepath):
    with open(filepath, 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(headers)
        for record in data:
            csv_writer.writerow(record.values())

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

def answer_vote(answer_id, vote):
    answers = get_all_answers()
    for i, answer in enumerate(answers):
        if answer['id'] == answer_id:
            question_id = answer['question_id']
            vote_number = int(answers[i]['vote_number'])
            vote_number += vote
            answers[i]['vote_number'] = vote_number

    with open(ANSWERS_DATA, 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(ANSWER_HEADER)
        for answer in answers:
            csv_writer.writerow(answer.values())

    return question_id

def save_all(all_questions):
    with open(QUESTIONS_DATA, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=QUESTION_HEADER)
        writer.writeheader()
        writer.writerows(all_questions)

def count_views(question_id):
    questions = get_all_questions()
    updated_list = []
    for row in questions:
        if row['id'] == question_id:
            row['view_number'] = int(row['view_number']) + 1
        updated_list.append(row)
    save_all(updated_list)
