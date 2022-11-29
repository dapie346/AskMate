import data_handler
import database_common

ANSWERS_DATA = 'answer'
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'user', 'message', 'image']


@database_common.connection_handler
def get_answers(cursor):
    query = f"""
        SELECT *
        FROM answer"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_to_question(cursor, question_id):
    query = f"""
        SELECT *
        FROM answer
        WHERE question_id = %(q_id)s"""
    cursor.execute(query, {'q_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def add_answer(cursor, answer, question_id, files):
    if files['image'].filename != '':
        image = f'answer_{id}.png'
        data_handler.save_image(files['image'], f'answer_{id}.png')
    else:
        image = ''

    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, username, message, image)
        VALUES (NOW(), %(vn)s, %(q_id)s, %(un)s, %(msg)s, %(img)s)"""
    cursor.execute(
        query,
        {
            'vn': 0,
            'q_id': question_id,
            'un': answer['user'],
            'msg': answer['message'],
            'img': image
        }
    )


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = """
        DELETE FROM answer
        WHERE id = %{id}s"""
    cursor.execute(query, {'id': answer_id})


@database_common.connection_handler
def answer_vote(cursor, answer_id, vote):
    query = """
        UPDATE answer
        SET vote_number = vote_number+%(vn)s
        WHERE id = %(id)s
        RETURNING question_id"""
    cursor.execute(query, {'vn': vote, 'id': answer_id})
    return cursor.fetchone()
