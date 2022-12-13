import database_common


@database_common.connection_handler
def get_tags(cursor):
    query = f"""
            SELECT *
            FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_tags_and_counts(cursor):
    query = """
        SELECT tag.name, COUNT(qt.question_id) AS tag_count
        FROM tag
        JOIN question_tag qt on tag.id = qt.tag_id
        GROUP BY tag.id
    """
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
            SELECT tag.name, tag.id
            FROM question_tag INNER JOIN tag ON question_tag.tag_id = tag.id
            WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()

@database_common.connection_handler
def remove_tag(cursor, question_id, tag_id):
    query = """
            DELETE FROM question_tag
            WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s"""
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})

def get_tag_names_from_list(tag_list):
    return [tag['name'] for tag in tag_list]