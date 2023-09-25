import mysql.connector
from mysql.connector import Error


def connect():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host='encounter-do-user-14509779-0.b.db.ondigitalocean.com',
                                       database='defaultdb',
                                       user='doadmin',
                                       password='AVNS_Lp2BBCOdyJ1JPWM2wtj')
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == '__main__':
    connect()