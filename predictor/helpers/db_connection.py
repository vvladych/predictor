
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
        dbInstance = psycopg2.connect(host="%s" % config.get(dbconn, 'host'),
                                      port="%s" % config.get(dbconn, 'port'),
                                      dbname="%s" % config.get(dbconn, 'dbname'),
                                      user="%s" % config.get(dbconn, 'user'),
                                      password="%s" % config.get(dbconn, 'password'))
    return dbInstance

    
def get_uuid_from_database():
    with dbcursor_wrapper("SELECT uuid_generate_v4() as uuid") as cursor:
        rows = cursor.fetchall()
        return rows[0].uuid


def enum_retrieve_valid_values(enum_type):
    enum_values_list = []
    cur = get_db_connection().cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute("""
            select
                e.enumlabel as enum_value
            from
                pg_type t
            join
                pg_enum e
            on
                t.oid = e.enumtypid
            join
                pg_catalog.pg_namespace n
            ON
                n.oid = t.typnamespace
            where
                t.typname='%s'
            """ % enum_type)
    counter = 0
    for enum_values in cur.fetchall():
        enum_values_list.append([counter, enum_values.enum_value])
        counter += 1
    cur.close()
    return enum_values_list
