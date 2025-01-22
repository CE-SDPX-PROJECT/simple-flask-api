import mysql.connector
from os import getenv

def ConnectorMysql():
  try:
    print(f"Connecting to database: {getenv('MYSQL_HOST')}")
    database = mysql.connector.connect(
      host=getenv("MYSQL_HOST"),
      user=getenv("MYSQL_USER"),
      passwd=getenv("MYSQL_PASSWORD"),
      database=getenv("MYSQL_DATABASE"),
      auth_plugin='mysql_native_password'
    )

    return database

  except Exception as error:
    print(f'Error connecting to database: {error}')
    return
  
def validate_user_input(data):
  if not data:
    return 'No input data provided', False, 400
  if 'name' not in data or not data['name']:
    return 'Name is required', False, 400
  if 'age' not in data:
    return 'Age is required', False, 400
  try:
    age = int(data['age'])
    if age <= 0:
      return 'Age must be a positive integer', False, 400
  except ValueError:
      return 'Age must be an integer', False, 400
  return None, True, 200

def get_all(table):
  database = ConnectorMysql()
  cursor = database.cursor()
  
  cursor.execute(f"SELECT * FROM {table}")
  result = cursor.fetchall()

  cursor.close()
  database.close()

  return result

def get_by_id(table, id):
  database = ConnectorMysql()
  cursor = database.cursor()
  
  cursor.execute(f"SELECT * FROM {table} WHERE uid=%s", (id,))
  result = cursor.fetchone()

  cursor.close()
  database.close()

  return result

def insert(table, data):
  database = ConnectorMysql()
  cursor = database.cursor()
  
  columns = ', '.join(data.keys())
  values = ', '.join(['%s']*len(data))
  
  cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})", tuple(data.values()))
  database.commit()

  cursor.close()
  database.close()

  return cursor.lastrowid

def update(table, id, data):
  database = ConnectorMysql()
  cursor = database.cursor()
  
  columns = ', '.join([f"{col}=%s" for col in data.keys()])
  
  cursor.execute(f"UPDATE {table} SET {columns} WHERE uid=%s", tuple(data.values()) + (id,))
  database.commit()

  cursor.close()
  database.close()

  return cursor.rowcount

def delete(table, id):
  database = ConnectorMysql()
  cursor = database.cursor()
  
  cursor.execute(f"DELETE FROM {table} WHERE uid=%s", (id,))
  database.commit()

  cursor.close()
  database.close()

  return cursor.rowcount