import os
import csv
import random

IMAGE_FOLDER = 'static/images'


def get_records(filepath):
    with open(filepath, 'r') as file:
        dict_reader = csv.DictReader(file)
        list_of_dict = list(dict_reader)
        for record in list_of_dict:
            for k, v in record.items():
                if k == 'view_number':
                    record[k] = int(record[k])
                elif k == 'vote_number':
                    record[k] = int(record[k])
    return list_of_dict


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


def generate_id(csv_data):
    while True:
        id = random.randint(1000, 9999)
        if not any(id == record['id'] for record in csv_data):
            return id