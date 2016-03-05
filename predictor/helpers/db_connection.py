
import psycopg2
from predictor.helpers import config

__all__ = ['get_db_connection']

dbInstance = None
dbconn = config.get('profile', 'dbconn')


class dbcursor_wrapper:
    def __init__(self, query, data=None):
        self.query = query
        self.data = data

    def __enter__(self):
        self.cursor = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        self.cursor.execute(self.query, self.data)
        return self.cursor
        
    def __exit__(self, t, value, traceback):
        self.cursor.close()


def get_db_connection():
    global dbInstance
    if dbInstance is None:
        dbInstance = psycopg2.connect("""dbname=%s user=%s password=%s""" %
                                      (config.get(dbconn, 'dbname'),
                                       config.get(dbconn, 'user'),
                                       config.get(dbconn, 'password')))
    return dbInstance

    
def get_uuid_from_database():
    with dbcursor_wrapper("SELECT uuid_generate_v4() as uuid") as cursor:
        rows = cursor.fetchall()
        return rows[0].uuid
