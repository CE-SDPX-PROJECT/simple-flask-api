from flask import Flask, request, jsonify
from db import validate_user_input, get_all, get_by_id, insert, update, delete
from dotenv import load_dotenv
from utils import convert_users_to_dict, convert_user_to_dict

load_dotenv()

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    print('Health check')
    return jsonify({'status': 'healthy'})

@app.route('/user', methods=['GET'])
def get_users():
    try:
        users = get_all('USERS')
        return jsonify(convert_users_to_dict(users)), 200
    except Exception as error:
        print(f'Error getting users: {error}')
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = get_by_id('USERS', user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(convert_user_to_dict(user)), 200
    except Exception as error:
        print(f'Error getting user: {error}')
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        error_message, valid, status = validate_user_input(data)

        if not valid:
            return jsonify({'error': error_message}), status
        
        user_id = insert('USERS', data)

        return jsonify({'message': 'User created successfully', 'uid': user_id}), 201
    
    except Exception as error:
        print(f'Error creating user: {error}')
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()

        error_message, valid, status = validate_user_input(data)

        if not valid:
            return jsonify({'error': error_message}), status
        
        updated = update('USERS', user_id, data)

        if not updated:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': f'User {user_id} updated successfully'}), 200
    except Exception as error:
        print(f'Error updating user: {error}')
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        deleted = delete('USERS', user_id)

        if not deleted:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': f'User {user_id} deleted successfully'}), 200
    except Exception as error:
        print(f'Error deleting user: {error}')
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)