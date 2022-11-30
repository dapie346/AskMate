import os
import database_common

IMAGE_FOLDER = 'static/images'


@database_common.connection_handler
def read_from_table(cursor, table):
    query = f"""
            SELECT *
            FROM {table}"""
    cursor.execute(query)
    return cursor.fetchall()


def save_image(file, filename):
    file.save(os.path.join(IMAGE_FOLDER, filename))


def delete_image(filename):
    os.remove(os.path.join(IMAGE_FOLDER, filename))


@database_common.connection_handler
def search_for(cursor, value):
    cursor.execute("""
        SELECT id,message,title,view_number,vote_number,submission_time
        FROM question
        WHERE title LIKE '%%' || %s || '%%' OR  message LIKE '%%' || %s || '%%' 
    """, [value, value]
    )
    return cursor.fetchall()


@database_common.connection_handler
def search_for_answer(cursor, value):
    cursor.execute("""
        SELECT id,message,question_id
        FROM answer
        WHERE message LIKE '%%' || %s || '%%' 
    """, [value]
    )
    return cursor.fetchall()
