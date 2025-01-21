from flask import Flask, request, jsonify
from db import get_all, get_by_id, insert, update, delete
from dotenv import load_dotenv
from utils import convert_users_to_dict, convert_user_to_dict

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    print('Health check')
    return jsonify({'status': 'healthy'})

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = get_all('USERS')
        return jsonify(convert_users_to_dict(users)), 200
    except Exception as error:
        print(f'Error getting users: {error}')
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = get_by_id('USERS', user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(convert_user_to_dict(user)), 200
    except Exception as error:
        print(f'Error getting user: {error}')
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.
    except:
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, host="0.0.0.0", port=5000)