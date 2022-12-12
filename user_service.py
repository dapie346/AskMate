import data_handler
import database_common


@database_common.connection_handler
def register_new_user(cursor, username, email, password):
    query = f"""
        INSERT INTO "user" (username, email, password, registration_date)
        VALUES (%(username)s, %(email)s, %(password)s, NOW()::TIMESTAMP(0))"""
    cursor.execute(query, {'username': username, 'email': email, 'password': password})


@database_common.connection_handler
def check_user_email(cursor, email):
    query = f"""
        SELECT email
        FROM "user"
        WHERE email = %(email)s
        """
    cursor.execute(query, {'email': email})
    return cursor.fetchone()


@database_common.connection_handler
def get_user_from_username(cursor, username):
    query = f'''
        SELECT *
        FROM "user"
        WHERE username = %(username)s'''
    cursor.execute(query, {'username': username})
    return cursor.fetchone()


def get_all_users(cursor):
    query = f'''
        SELECT "user".username,
       "user".registration_date,
       COUNT(DISTINCT q.id) AS question_count,
       COUNT(DISTINCT a.id) AS answer_count,
       COUNT(DISTINCT c.id) AS comment_count,
       10 AS reputation
        FROM "user"
        JOIN question q on "user".id = q.user_id
        JOIN answer a on "user".id = a.user_id
        JOIN comment c on "user".id = c.user_id
        GROUP BY "user".id;'''
    cursor.execute(query)
    return cursor.fetchall()