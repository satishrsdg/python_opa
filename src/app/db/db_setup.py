import sqlite3
import json
from . import TABLES

def create_connection():
  conn = None
  try:
    conn = sqlite3.connect('./src/app/db/products.db')
    conn.row_factory = convert_dbrows_to_dict
  except sqlite3.Error as  e:
    print(e)

  return conn

def clean_up(conn):
  c = conn.cursor()
  # for table in TABLES.TABLES:
  #   c.execute('DROP TABLE IF EXISTS ' + table['name'])
  c.close()

def initialize_schema(conn):
  c = conn.cursor()
  for table in TABLES.TABLES:
      c.execute('DROP TABLE IF EXISTS ' + table['name'])
      c.execute(table['schema'])
  conn.commit()

def convert_dbrows_to_dict(cursor, row):
  return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))

def initialize_db(conn):
  initialize_schema(conn)
  populate_data(conn)
  

def populate_data(conn):
  cur = conn.cursor()
  for table in TABLES.TABLES:
      for row in table['data']:
        insert_object(table['name'], cur, row)
  conn.commit()

ii = 0
def insert_object(table, cursor, obj):
  row_keys = sorted(obj.keys())
  keys = '(' + ','.join(row_keys) + ')'
  values = '(' + ','.join(['?'] * len(row_keys)) + ')'
  stmt = 'INSERT INTO {} {} VALUES {}'.format(table, keys, values)
  args = [str(obj[k]) for k in row_keys]
  global ii
  ii += 1
  if (ii % 100 == 0):
    print("%s %s"%(str(stmt), args))
  cursor.execute(stmt, args)

def query_database(conn, query, args=(), one=False):
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_all_products(conn):
  return query_database(conn, "select * from products;")

def get_restricted_products(conn, query):
  return query_database(conn, query)

def get_products_of_assistant(conn, category_assistant):
  return query_database(conn, "select * from products where category_assistant = ?", args=(category_assistant,))
