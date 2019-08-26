
def test_table_product_exists(connection, populate_db):
  print('test_table_product_exists')
  stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='products';"
  cursor = connection.execute(stmt)
  rs = cursor.fetchall()
  assert len(rs) == 1
    