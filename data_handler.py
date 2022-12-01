import os
import database_common
import question_service

IMAGE_FOLDER = 'static/images'


def save_image(file, filename):
    file.save(os.path.join(os.path.abspath(IMAGE_FOLDER), filename))


def delete_image(filename):
    os.remove(os.path.join(os.path.abspath(IMAGE_FOLDER), filename))


@database_common.connection_handler
def search_through_questions(cursor, value):
    cursor.execute("""
        SELECT *
        FROM question
        WHERE title ILIKE '%%' || %s || '%%' OR  message LIKE '%%' || %s || '%%' 
    """, [value, value]
    )
    return cursor.fetchall()


@database_common.connection_handler
def search_through_answers(cursor, value):
    cursor.execute("""
        SELECT question_id,message
        FROM answer
        WHERE message ILIKE '%%' || %s || '%%' 
    """, [value]
    )
    answers = cursor.fetchall()
    print(answers)
    questions = []
    for i in answers:
        questions.append(question_service.get_question(i['question_id']))
    return questions


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