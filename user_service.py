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


@database_common.connection_handler
def get_all_users(cursor):
    query = f'''
        WITH cte_reputation AS (
        SELECT
        "user".id,
        COALESCE((SELECT SUM(value) FROM question_vote LEFT JOIN question q on question_vote.question_id = q.id WHERE q.user_id = "user".id), 0)
        +
        COALESCE((SELECT SUM(value) FROM answer_vote LEFT JOIN answer a on answer_vote.answer_id = a.id WHERE a.user_id = "user".id), 0)
        +
        (SELECT COUNT(id) * 15 FROM answer WHERE user_id = "user".id AND accepted)
        as reputation
        FROM "user"
        GROUP BY "user".id
        )       
        SELECT "user".username,
       "user".registration_date,
       "user".id,
       COUNT(DISTINCT q.id) AS question_count,
       COUNT(DISTINCT a.id) AS answer_count,
       COUNT(DISTINCT c.id) AS comment_count,
        cte_reputation.reputation
        FROM "user"
        LEFT JOIN question q on "user".id = q.user_id
        LEFT JOIN answer a on "user".id = a.user_id
        LEFT JOIN comment c on "user".id = c.user_id
        LEFT JOIN cte_reputation on "user".id = cte_reputation.id
        GROUP BY "user".id, cte_reputation.reputation;'''
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_from_id(cursor, id):
    query = f'''
        WITH cte_reputation AS (
        SELECT
        "user".id,
        COALESCE((SELECT SUM(value) FROM question_vote LEFT JOIN question q on question_vote.question_id = q.id WHERE q.user_id = "user".id), 0)
        +
        COALESCE((SELECT SUM(value) FROM answer_vote LEFT JOIN answer a on answer_vote.answer_id = a.id WHERE a.user_id = "user".id), 0)
        +
        (SELECT COUNT(id) * 15 FROM answer WHERE user_id = "user".id AND accepted)
        as reputation
        FROM "user"
        GROUP BY "user".id
        )  
        SELECT "user".id, 
        "user".username,
        "user".registration_date,
        COUNT(DISTINCT q.id) AS question_count,
        COUNT(DISTINCT a.id) AS answer_count,
        COUNT(DISTINCT c.id) AS comment_count,
        cte_reputation.reputation
        FROM "user"
            LEFT JOIN question q on "user".id = q.user_id
            LEFT JOIN answer a on "user".id = a.user_id
            LEFT JOIN comment c on "user".id = c.user_id
            LEFT JOIN cte_reputation on "user".id = cte_reputation.id
        WHERE "user".id = %(id)s
        GROUP BY "user".id, cte_reputation.reputation;
    '''
    cursor.execute(query, {'id': id})
    return cursor.fetchone()
