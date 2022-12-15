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
            SELECT * FROM calculate_reputation()
        )
        , cte_counts AS (
            SELECT * FROM get_user_counts()
        )
        SELECT "user".username,
       "user".registration_date,
       "user".id,
       cte_counts.question_count,
       cte_counts.answer_count,
       cte_counts.comment_count,
        cte_reputation.reputation
        FROM "user"
        LEFT JOIN cte_counts on "user".id = cte_counts.id
        LEFT JOIN cte_reputation on "user".id = cte_reputation.id
        GROUP BY "user".id, cte_reputation.reputation, cte_counts.question_count, cte_counts.answer_count, cte_counts.comment_count;'''
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_from_id(cursor, id):
    query = f'''
            WITH cte_reputation AS (
                SELECT * FROM calculate_reputation()
            )
            , cte_counts AS (
                SELECT * FROM get_user_counts()
            )
            SELECT "user".username,
           "user".registration_date,
           "user".id,
           cte_counts.question_count,
           cte_counts.answer_count,
           cte_counts.comment_count,
            cte_reputation.reputation
            FROM "user"
            LEFT JOIN cte_counts on "user".id = cte_counts.id
            LEFT JOIN cte_reputation on "user".id = cte_reputation.id
            WHERE "user".id = %(id)s
            GROUP BY "user".id, cte_reputation.reputation, cte_counts.question_count, cte_counts.answer_count, cte_counts.comment_count;'''
    cursor.execute(query, {'id': id})
    return cursor.fetchone()
