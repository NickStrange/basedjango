# import sqlite3
from django.db import connection


def set_seq(seq_name: str, val: str) -> None:
    """
    reset the sequence named seq_name to val

    :param seq_name:
    :param val:
    :return:
    """
    command = f"ALTER SEQUENCE {seq_name}_id_seq RESTART WITH {val}"
    print('set id', command)
    # connection_db = sqlite3.connect('db.sqlite3')
    # table_connection_db = connection_db.cursor()
    cursor = connection.cursor()
    # table_connection_db.execute(f"UPDATE sqlite_sequence set seq ={val} WHERE name = '{seq_name}'")
    cursor.execute(command)
    # connection_db.commit()
    # connection_db.close()
    print('set id', command)