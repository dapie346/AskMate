from csv import DictReader

QUESTIONS_DATA = 'sample_data/question.csv'
ANSWERS_DATA = 'sample_data/answer.csv'


def get_all_user_story():
    with open('sample_data/question.csv', 'r') as f:
        dict_reader = DictReader(f)

        list_of_dict = list(dict_reader)

    return list_of_dict


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
