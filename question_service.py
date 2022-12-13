import data_handler
import database_common


@database_common.connection_handler
def get_questions(cursor, order_by='submission_time', additions=''):
    query = f"""
        SELECT question.*, COALESCE(SUM(CASE WHEN qv.value IS NULL THEN NULL WHEN qv.value >= 0 THEN 1 ELSE -1 END), 0) as vote_number
        FROM question
        LEFT JOIN question_vote qv on question.id = qv.question_id
        GROUP BY question.id
        ORDER BY {order_by} {additions}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question(cursor, question_id):
    query = f"""
                SELECT question.*, COALESCE(SUM(CASE WHEN qv.value IS NULL THEN NULL WHEN qv.value >= 0 THEN 1 ELSE -1 END), 0) as vote_number
                FROM question
                LEFT JOIN question_vote qv on question.id = qv.question_id
                WHERE id = %(question_id)s
                GROUP BY question.id"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def add_question(cursor, user_id, question, files):
    query = """
                INSERT INTO question (submission_time, view_number, user_id, title, message)
                VALUES (NOW()::TIMESTAMP(0), 0, %(user)s, %(title)s, %(message)s)
                RETURNING id"""
    cursor.execute(query, {'user': user_id, 'title': question['title'], 'message': question['message']})
    id = cursor.fetchone()['id']
    if files['image'].filename != '':
        data_handler.save_image(files['image'], f'question_{id}.png')
        query = """
                        UPDATE question
                        SET image = %(image)s
                        WHERE id = %(question_id)s"""
        cursor.execute(query, {'question_id': id, 'image': f'question_{id}.png'})
    return id


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = """
                DELETE FROM question
                WHERE id = %(question_id)s
                RETURNING image"""
    cursor.execute(query, {'question_id': question_id})
    image = cursor.fetchone()['image']
    if image is not None:
        try:
            data_handler.delete_image(image)
        except FileNotFoundError:
            pass


@database_common.connection_handler
def question_vote(cursor, user_id, question_id, vote):
    query = """
            INSERT INTO question_vote AS qv (user_id, question_id, value) VALUES (%(user_id)s, %(question_id)s, %(vote)s)
            ON CONFLICT (user_id, question_id) DO 
            UPDATE SET value = %(vote)s 
            WHERE qv.user_id = %(user_id)s AND qv.question_id = %(question_id)s"""
    cursor.execute(query, {'user_id': user_id, 'question_id': question_id, 'vote': vote})


@database_common.connection_handler
def update_question(cursor, question_id, title, message):
    query = """
                UPDATE question
                SET title = %(title)s, message = %(message)s
                WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id, 'title': title, 'message': message})


@database_common.connection_handler
def count_views(cursor, question_id):
    query = """
            UPDATE question
            SET view_number = view_number + 1
            WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def tag_question(cursor, question_id, tag_id):
    query = """
            INSERT INTO question_tag (question_id, tag_id)
            VALUES (%(question_id)s, %(tag_id)s)"""
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})
