import data_handler
import database_common


@database_common.connection_handler
def get_user_from_username(cursor, name):
    query = f'''
        SELECT *
        FROM "user"
        WHERE username = %{name}s'''
    cursor.execute(query, {'name': name})
    return cursor.fetchone()


