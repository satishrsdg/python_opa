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
  return render_template('index.html', message="Hello world")

@app.route('/api/products/', methods=["GET"])
def get_all_products():
  return flask.jsonify(db_setup.get_all_products(get_conn()));

@app.route('/api/products/<category_assistant>', methods=["GET"])
@app.route('/api/products/<category_assistant>/', methods=["GET"])
def api_get_static_resource(category_assistant):
  user_name =  request.args['user_name']
  if user_name is None:
    user_name = ""
  
  path_list = request.path.strip("/").split("/")
  input_dict = { "input": {
        "user_name": user_name,
        "path": path_list,
        "method": request.method }}

  if access.is_access_allowed(input_dict, 'allow_static'):
     return render_template('image.html', user_name=user_name)
  else:
     return render_template('image.html', user_name="access_denied")

@app.route('/api/products/', methods=["POST"])
def get_restricted_products():
  data=request.get_json()
  if access.is_access_allowed(data, 'allow_list_check'):
    sql = access.compile(data)
    return flask.jsonify(db_setup.get_restricted_products(get_conn(),sql));
  else:
    return render_template('image.html', user_name="access_denied")

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