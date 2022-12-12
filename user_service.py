import database_common


@database_common.connection_handler
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