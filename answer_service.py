import data_handler
import database_common


@database_common.connection_handler
def get_answers(cursor):
    query = f"""
        SELECT *, COALESCE(SUM(CASE WHEN av.value IS NULL THEN NULL WHEN av.value >= 0 THEN 1 ELSE -1 END), 0) as vote_number
        FROM answer
        LEFT JOIN answer_vote av on answer.id = av.answer_id
        GROUP BY answer.id"""
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
        WITH cte_votes AS (
            SELECT answer.id, COALESCE(SUM(CASE WHEN av.value IS NULL THEN NULL WHEN av.value >= 0 THEN 1 ELSE -1 END), 0) as vote_number
            FROM answer
            LEFT JOIN answer_vote av on answer.id = av.answer_id
            GROUP BY answer.id
        )
        SELECT *, cte_votes.vote_number
        FROM answer
        JOIN "user"
            ON answer.user_id = "user".id
        LEFT JOIN cte_votes ON answer.id = cte_votes.id
        WHERE question_id = %(q_id)s
        GROUP BY answer.id, "user".id, cte_votes.id, cte_votes.vote_number
        ORDER BY cte_votes.vote_number DESC"""
    cursor.execute(query, {'q_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def add_answer(cursor, answer, question_id, user_id, files):
    query = """
        INSERT INTO answer (submission_time, question_id, user_id, message, accepted)
        VALUES (NOW()::TIMESTAMP(0), %(q_id)s, %(un)s, %(msg)s, false)
        RETURNING id"""
    cursor.execute(
        query,
        {
            'q_id': question_id,
            'un': user_id,
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
def answer_vote(cursor, user_id, answer_id, vote):
    query = """
                INSERT INTO answer_vote AS av (user_id, answer_id, value) VALUES (%(user_id)s, %(answer_id)s, %(vote)s)
                ON CONFLICT (user_id, answer_id) DO 
                UPDATE SET value = %(vote)s 
                WHERE av.user_id = %(user_id)s AND av.answer_id = %(answer_id)s"""
    cursor.execute(query, {'user_id': user_id, 'answer_id': answer_id, 'vote': vote})
    query = """
        SELECT question_id
        FROM answer
        WHERE id = %(answer_id)s
    """
    cursor.execute(query, {'answer_id': answer_id})
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


@database_common.connection_handler
def toggle_accepted_answer_status(cursor, answer_id):
    query = """
        UPDATE answer
        SET accepted = NOT accepted
        WHERE id = %(answer_id)s
        RETURNING question_id"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()['question_id']
