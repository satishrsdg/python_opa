import pytest
import src.app.db.db_setup as db_setup

@pytest.fixture(scope='module')
def connection():
  print('----Connection---')
  cnxn = db_setup.create_connection();
  yield cnxn

@pytest.fixture(scope='module')
def populate_db(connection):
  print('----Populate Db---')  
  db_setup.populate_data(connection)
  yield connection
  print('----Tear down---')  
  db_setup.clean_up(connection)





