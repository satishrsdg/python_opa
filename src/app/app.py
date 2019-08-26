import base64
import json
import flask
import os
from flask import request
from flask_bootstrap import Bootstrap
from flask import g
from flask import render_template

from src.app.db import db_setup as db_setup
from src.app.authz import access as access

app = flask.Flask(__name__)
Bootstrap(app)
conn = None

def get_conn():
  conn = getattr(g, '_conn', None)
  if conn is None:
    conn = g._conn = db_setup.create_connection();
  return conn;

@app.route('/', methods=["GET"])
def index():
  print("hello world")
  return render_template('index.html', message="hello world")

@app.route('/api/products/<category_assistant>/', methods=["POST"])
def api_get_post(category_assistant):
  data=request.get_json()
  data['input']['path'] = ["api","products",category_assistant]
  if access.is_access_allowed(data):
    return flask.jsonify(db_setup.get_products_of_assistant(get_conn(), category_assistant))
  else:
    return { "result": "access denied"}

@app.route('/api/products/', methods=["GET"])
def get_all_products():
  return flask.jsonify(db_setup.get_all_products(get_conn()));

@app.route('/api/products/', methods=["POST"])
def get_restricted_products():
  data=request.get_json()
  print(data)
  sql = access.compile(data)
  return flask.jsonify(db_setup.get_restricted_products(get_conn(),sql));

@app.teardown_appcontext
def close_connection(e):
  print('tear down')
  db_setup.clean_up(get_conn())

def main():
  with app.app_context():
    db_setup.initialize_db(get_conn());
    
  app.jinja_env.auto_reload = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  print(os.environ['PY_PORT'])
  app.run(host="0.0.0.0", port=os.environ['PY_PORT'], debug=True)

if __name__ == '__main__':
  main()