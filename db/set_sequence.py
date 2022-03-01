import sqlite3


def set_seq(seq_name: str, val: str) -> None:
    """
    reset the sequence named seq_name to val

    :param seq_name:
    :param val:
    :return:
    """
    connection_db = sqlite3.connect('db.sqlite3')
    table_connection_db = connection_db.cursor()
    table_connection_db.execute(f"UPDATE sqlite_sequence set seq ={val} WHERE name = '{seq_name}'")
    connection_db.commit()
    connection_db.close()
    print('set id', f"UPDATE sqlite_sequence set seq ={val} WHERE name ={seq_name}")