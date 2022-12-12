import data_handler
import database_common


@database_common.connection_handler
def register_new_user(cursor, username, email, password):
    query = f"""
        INSERT INTO "user" (username, email, password)
        VALUES (%(username)s, %(email)s, %(password)s)"""
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
def check_username(cursor, username):
    query = f"""
        SELECT username
        FROM "user"
        WHERE username = %(username)s
        """
    cursor.execute(query, {'username': username})
    return cursor.fetchone()
def get_user_from_username(cursor, name):
    query = f'''
        SELECT *
        FROM "user"
        WHERE username = %{name}s'''
    cursor.execute(query, {'name': name})
    return cursor.fetchone()


