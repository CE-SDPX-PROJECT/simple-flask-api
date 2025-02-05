import mysql.connector
import os
from mysql.connector import Error

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    return connection

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
 
def add_user(name, age):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO USERS (name, age) VALUES (%s, %s)', (name, age))
        connection.commit()
        connection.close()
        return {'message': 'User added successfully'}, None, 201
    except Error as e:
        return None, str(e), 500
def update_user(uid, name=None, age=None):
    update_fields = []
    update_values = []
    validation_errors = []

    if name is not None:
        try:
            if not isinstance(name, str):
                validation_errors.append('Name must be a string')
            else:
                name = str(name)
                update_fields.append("name = %s")
                update_values.append(name)
        except ValueError:
            validation_errors.append('Name must be a string')

    if age is not None:
        try:
            if isinstance(age, str):
                validation_errors.append('Age must be an integer')
            else:
                age = int(age)
                if age <= 0:
                    validation_errors.append('Age must be a positive integer')
                else:
                    update_fields.append("age = %s")
                    update_values.append(age)
        except ValueError:
            validation_errors.append('Age must be an integer')

    if validation_errors:
        return None, '\n'.join(validation_errors), 400

    if not update_fields:
        return {'message': 'User updated successfully'}, None, 200

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        update_values.append(uid)

        query = f"UPDATE USERS SET {', '.join(update_fields)} WHERE uid = %s"
        cursor.execute(query, tuple(update_values))
        connection.commit()

        connection.close()

        return {'message': 'User updated successfully'}, None, 200
    except Error as e:
        return None, str(e), 500

def delete_user(uid):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM USERS WHERE uid = %s', (uid,))
        connection.commit()
        connection.close()
        return {'message': 'User deleted successfully'}, None, 200
    except Error as e:
        return None, str(e), 500

def get_all_users():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT uid, name, age FROM USERS')
        users = cursor.fetchall()
        connection.close()
        return users, None, 200
    except Error as e:
        return None, str(e), 500

def get_user_by_id(uid):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT uid, name, age FROM USERS WHERE uid = %s', (uid,))
        user = cursor.fetchone()
        connection.close()
        if user:
            return user, None, 200
        else:
            return None, 'User not found', 404
    except Error as e:
        return None, str(e), 500
