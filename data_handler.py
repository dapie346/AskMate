from csv import DictReader


def get_all_user_story():
    with open('sample_data/question.csv', 'r') as f:
        dict_reader = DictReader(f)

        list_of_dict = list(dict_reader)

    return list_of_dict