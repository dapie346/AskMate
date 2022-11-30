import data_handler
import database_common

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


@database_common.connection_handler
def get_questions(cursor, order_by, additions):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {order_by} {additions}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question(cursor, question_id):
    query = f"""
                SELECT *
                FROM question
                WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def add_question(cursor, question, files):
    image_filename = files['image'].filename
    query = """
                INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                VALUES (NOW(), 0, 0, %(title)s, %(message)s, %(image)s)
                RETURNING id"""
    cursor.execute(query, {'title': question['title'], 'message': question['message'], 'image': image_filename if image_filename != '' else None})
    if image_filename != '':
        data_handler.save_image(files['image'], image_filename)
    return cursor.fetchone()['id']


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
def question_vote(cursor, question_id, vote):
    query = """
            UPDATE question
            SET vote_number = vote_number + %(vote)s
            WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id, 'vote': vote})


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
