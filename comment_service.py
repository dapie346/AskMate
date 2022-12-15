import database_common


@database_common.connection_handler
def add_to_question(cursor, user_id, message, question_id):
    query = """
        INSERT INTO comment 
        (question_id, user_id, message, submission_time, edited_count)
        VALUES (%(q_id)s, %(u_id)s, %(msg)s, NOW()::TIMESTAMP(0), %(ed_count)s)
        """
    cursor.execute(query, {'q_id': question_id, 'u_id': user_id, 'msg': message, 'ed_count': 0})


@database_common.connection_handler
def add_to_answer(cursor, user_id, message, question_id, answer_id):
    query = f"""
        INSERT INTO comment 
        (question_id, answer_id, user_id, message, submission_time, edited_count)
        VALUES (%(q_id)s, %(a_id)s, %(u_id)s, %(msg)s, NOW()::TIMESTAMP(0), %(ed_count)s)
        """
    cursor.execute(query, {'q_id': question_id, 'u_id': user_id, 'a_id': answer_id, 'msg': message, 'ed_count': 0})


@database_common.connection_handler
def delete_comment(cursor, comment):
    query = """
        DELETE FROM comment
        WHERE id = %(comment_id)s
        """
    cursor.execute(query, {'comment_id': comment['id']})


@database_common.connection_handler
def edit_comment(cursor, comment, message):
    query = """
        UPDATE comment
        SET message = %(message)s,
        submission_time = NOW()::TIMESTAMP(0),
        edited_count = edited_count+1
        WHERE id = %(comment_id)s"""
    cursor.execute(query, {'comment_id': comment['id'], 'message': message})


@database_common.connection_handler
def get_comment(cursor, comment_id):
    query = f"""
        SELECT *
        FROM comment
        WHERE id = %(comment_id)s"""
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_comments_to_question(cursor, question_id):
    query = f"""
        SELECT *
        FROM comment
        WHERE question_id = %(q_id)s
        AND answer_id IS NULL
        """
    cursor.execute(query, {'q_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_to_answers(cursor, question_id):
    query = f"""
        SELECT comment.*, username
        FROM comment
        JOIN "user" on "user".id = comment.user_id
        WHERE question_id = %(q_id)s
        AND answer_id IS NOT NULL
        """
    cursor.execute(query, {'q_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_user_comments(cursor, user_id):
    query = f'''
        SELECT message, question_id 
        FROM comment
        WHERE user_id = %(id)s
    '''
    cursor.execute(query, {'id': user_id})
    return cursor.fetchall()

@database_common.connection_handler
def get_comment_user_id(cursor, comment_id):
    query = f'''
            SELECT user_id 
            FROM comment
            WHERE id = %(comment_id)s
        '''
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()['user_id']