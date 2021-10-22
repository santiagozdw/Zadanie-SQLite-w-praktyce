import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def close_connection(conn):
    """ close a database connection to a SQLite database """
    if conn:
        conn.close()
    return conn

def create_todos_table(conn):
    """ create table
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    create_todos_sql = """
    -- todos table
    CREATE TABLE IF NOT EXISTS todos (
        id integer PRIMARY KEY,
        title text NOT NULL,
        description text,
        done boolean NOT NULL
    );
    """

    try:
        c = conn.cursor()
        c.execute(create_todos_sql)
    except Error as e:
        print(e)



def create_todo(conn, todo_title, todo_description, todo_done):
    sql = 'INSERT INTO todos(title, description, done) VALUES(?,?,?)'
    cur = conn.cursor()
    cur.execute(sql, (todo_title, todo_description, todo_done))
    conn.commit()
    return cur.lastrowid


def select_all_todos(conn):
    """Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM todos")
    rows = cur.fetchall()

    return rows

def select_todo_where(conn, query_param, query_param_value):
    """Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param query_param: one of todo attributes : id, title, done
    :param query_param_value: value of query_param - eg: select_todo_where(conn,'title', 'title1') 
    equals to SELECT * FROM todos WHERE title = title1
    :return:
    """
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM todos WHERE {query_param} = "{query_param_value}"')
    rows = cur.fetchall()
    return rows

def update_todo(conn, id, status):
    """
    update 'done' field of todo no 'id'
    :param conn:
    :param id: todo id
    :param status: 0 - not done, 1 - done
    :return: True if success
    """
    sql = f''' UPDATE todos
                SET done = {status}
                WHERE id = {id}'''
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return True
    except sqlite3.OperationalError:
        return False

def delete_todo(conn, id):
    """
    delete todo no 'id'
    :param conn:
    :param id: todo id
    :return: True if success
    """
    sql = f''' DELETE FROM todos
                WHERE id = {id}'''
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return True
    except sqlite3.OperationalError:
        return False

if __name__ == '__main__':
   conn = create_connection(r"todos_database.db")
   create_todos_table(conn)
   print(select_all_todos(conn))
   print(select_todo_where(conn, 'done', 0))
   print(update_todo(conn, 1, 1))
   print(select_todo_where(conn, 'id', 1))
   print(delete_todo(conn, 1))
   print(select_all_todos(conn))
     
   close_connection(conn)
