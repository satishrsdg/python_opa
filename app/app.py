import base64
import json
import flask
import os
from flask import request
from flask_bootstrap import Bootstrap
from flask import g
from db import db_setup
from authz import access
from flask import render_template

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
  if conn is not None:
    conn.close()

if __name__ == '__main__':

  with app.app_context():
    db_setup.initialize_db(get_conn());
    
  app.jinja_env.auto_reload = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  print(os.environ['PY_PORT'])
  app.run(host="0.0.0.0", port=os.environ['PY_PORT'], debug=True)