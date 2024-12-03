

import pymysql


def create_connection( host, port, user_name, user_password):
    try:
        db = pymysql.connect(
            host=host,
            port=int(port),
            user=user_name,
            password=user_password,
        )
        cursor=db.cursor()
        return cursor
    except pymysql.MySQLError as e:

        return f"Error connecting to MySQL Platform: {e}"
    except Exception as e:

        return f"An unexpected error occurred: {e}"


def execute_query(cursor, query, params=None):
    try:
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        print("Query executed successfully")
    except :
        print(f"The error  occurred")


def show_databases(cursor):
    sql="show databases"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def show_tables(cursor,databases):
    sql="SELECT TABLE_NAME  FROM information_schema.tables  WHERE table_schema ='"+databases+"'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def get_data(cursor,sql):
    cursor.execute(sql)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    return column_names, rows





