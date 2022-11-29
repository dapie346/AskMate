import os
import csv
import random

IMAGE_FOLDER = 'static/images'
import database_common

@database_common.connection_handler
def read_from_table(cursor, table):
    query = f"""
            SELECT *
            FROM {table}"""
    cursor.execute(query)
    return cursor.fetchall()


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


@database_common.connection_handler
def search_for(cursor, value):
    cursor.execute(
    """
    SELECT id,message,title,view_number,vote_number,submission_time
    FROM question
    WHERE title LIKE '%%' || %s || '%%' OR  message LIKE '%%' || %s || '%%' 
    """, [value, value]
    )
    return cursor.fetchall()


@database_common.connection_handler
def search_for_answer(cursor, value):
    cursor.execute(
    """
    SELECT id,message,question_id
    FROM answer
    WHERE message LIKE '%%' || %s || '%%' 
    """, [value]
    )
    return cursor.fetchall()
