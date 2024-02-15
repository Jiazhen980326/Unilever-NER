import os.path
import sqlite3
from pymongo import MongoClient
import config

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

class DB(object):
    @staticmethod
    def conn():
        conn = sqlite3.connect(config.datapath)
        conn.row_factory = dict_factory
        return conn

    @staticmethod
    def create(schema):
        conn = DB.conn()
        with open(schema) as f:
            conn.executescript(f.read())
        conn.close()

    @staticmethod
    def query(q, p):
        conn = DB.conn()
        cursor = conn.cursor()
        data = cursor.execute(q, p).fetchall()
        conn.close()
        return data

    @staticmethod
    def insert(table, field, data):
        q = 'INSERT INTO ' + table + ' (' + ','.join(field) + \
            ') VALUES (' + ','.join(['?' for i in range(len(field))]) + ');'
        conn = DB.conn()
        cursor = conn.cursor()
        for d in data:
            res = cursor.execute(q, d)
        conn.commit()
        conn.close()
        print('inserted')

    @staticmethod
    def update(q, p):
        conn = DB.conn()
        cursor = conn.cursor()
        data = cursor.execute(q, p).fetchall()
        conn.commit()
        conn.close()
        return data

def fetchMGDB(constr, dbname, collection, idfield, docfield):
    client = MongoClient(constr)
    collection = client[dbname][collection]
    items = collection.find()
    data = []
    for item in items:
        data.append([item[idfield], item[docfield]])

    conn = DB.conn()
    cursor = conn.cursor()
    for d in data:
        q = 'INSERT INTO documents ( document_id, context, entity_fetched) VALUES ' \
            '(?, ?, 0)' 
        # print(q)
        try:
            data = cursor.execute(q, (str(d[0]), d[1]))
        except sqlite3.OperationalError:
            print('sqlite3OpError', str(d[0]))

    q = 'UPDATE input SET fetched = ? WHERE rowid = ( SELECT max(rowid) FROM input );'
    cursor.execute(q, (1,))
    conn.commit()
    conn.close()


