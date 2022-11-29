import database_common

@database_common.connection_handler
def get_tags(cursor):
    query = f"""
            SELECT *
            FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def add_tag(cursor, tag):
    query = f"""
            INSERT INTO tag (name)
            VALUES (%(name)s)
            RETURNING id"""
    cursor.execute(query, {'name': tag})
    return cursor.fetchone()['id']

@database_common.connection_handler
def get_question_tags(cursor, question_id):
    query = f"""
            SELECT tag.name
            FROM question_tag INNER JOIN tag ON question_tag.tag_id = tag.id
            WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    tags = cursor.fetchall()
    return [tag['name'] for tag in tags]