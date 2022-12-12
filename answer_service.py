import data_handler
import database_common


@database_common.connection_handler
def get_answers(cursor):
    query = f"""
        SELECT *
        FROM answer"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer(cursor, answer_id):
    query = f"""
        SELECT *
        FROM answer
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_answers_to_question(cursor, question_id):
    query = f"""
        SELECT *
        FROM answer
        WHERE question_id = %(q_id)s
        ORDER BY vote_number DESC"""
    cursor.execute(query, {'q_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def add_answer(cursor, answer, question_id, files):
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, username, message)
        VALUES (NOW()::TIMESTAMP(0), %(vn)s, %(q_id)s, %(un)s, %(msg)s)
        RETURNING id"""
    cursor.execute(
        query,
        {
            'vn': 0,
            'q_id': question_id,
            'un': answer['user'],
            'msg': answer['message']
        }
    )
    id = cursor.fetchone()['id']
    if files['image'].filename != '':
        data_handler.save_image(files['image'], f'answer_{id}.png')
        query = """
                UPDATE answer
                SET image = %(image)s
                WHERE id = %(answer_id)s"""
        cursor.execute(query, {'answer_id': id, 'image': f'answer_{id}.png'})


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = """
        DELETE FROM answer
        WHERE id = %(id)s
        RETURNING question_id, image"""
    cursor.execute(query, {'id': answer_id})
    query_returns = cursor.fetchone()
    image = query_returns['image']
    if image is not None:
        try:
            data_handler.delete_image(image)
        except FileNotFoundError:
            pass
    return query_returns['question_id']


@database_common.connection_handler
def answer_vote(cursor, answer_id, vote):
    query = """
        UPDATE answer
        SET vote_number = vote_number+%(vn)s
        WHERE id = %(id)s
        RETURNING question_id"""
    cursor.execute(query, {'vn': vote, 'id': answer_id})
    return cursor.fetchone()['question_id']


@database_common.connection_handler
def update_answer(cursor, answer_id, message):
    query = """
        UPDATE answer
        SET message = %(message)s
        WHERE id = %(answer_id)s
        RETURNING question_id"""
    cursor.execute(query, {'answer_id': answer_id, 'message': message})
    return cursor.fetchone()['question_id']
