import os
import database_common
import question_service

IMAGE_FOLDER = 'static/images'


def save_image(file, folder, filename):
    file.save(os.path.join(os.path.abspath(IMAGE_FOLDER + folder), filename))


def delete_image(folder, filename):
    os.remove(os.path.join(os.path.abspath(IMAGE_FOLDER + folder), filename))


@database_common.connection_handler
def search_through_questions(cursor, search):
    cursor.execute("""
        SELECT 
        question.id
        FROM question
        WHERE title ILIKE '%%' || %s || '%%' OR  message LIKE '%%' || %s || '%%' """, [search, search]
                   )
    questions = cursor.fetchall()
    return [question['id'] for question in questions]


@database_common.connection_handler
def search_through_answers(cursor, value):
    cursor.execute("""
        SELECT question_id
        FROM answer
        WHERE message ILIKE '%%' || %s || '%%' 
    """, [value]
                   )
    answers = cursor.fetchall()
    return [answer['question_id'] for answer in answers]


@database_common.connection_handler
def answers_for_question(cursor, value):
    cursor.execute("""
        SELECT question_id,message
        FROM answer
        WHERE message ILIKE '%%' || %s || '%%' 
    """, [value]
                   )
    answers = cursor.fetchall()
    return answers
