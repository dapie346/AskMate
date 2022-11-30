import os
import database_common
import question_service
IMAGE_FOLDER = 'static/images'

def save_image(file, filename):
    file.save(os.path.join(IMAGE_FOLDER, filename))

def delete_image(filename):
    os.remove(os.path.join(IMAGE_FOLDER, filename))

@database_common.connection_handler
def search_for(cursor, value):
    cursor.execute("""
        SELECT id,message,title,view_number,vote_number,submission_time
        FROM question
        WHERE title LIKE '%%' || %s || '%%' OR  message LIKE '%%' || %s || '%%' 
    """, [value, value]
    )
    return cursor.fetchall()


@database_common.connection_handler
def search_for_answer(cursor, value):
    cursor.execute("""
        SELECT question_id
        FROM answer
        WHERE message ILIKE '%%' || %s || '%%' 
    """, [value]
    )
    answers = cursor.fetchall()
    questions = []
    for i in answers:
        questions.append(question_service.get_question(i['question_id']))
    return questions
