from flask import Flask, request, jsonify
import os
from user import (validate_user_input as validate_user_input_service,
                  add_user as add_user_service,
                  update_user as update_user_service,
                  delete_user as delete_user_service,
                  get_all_users as get_all_users_service,
                  get_user_by_id as get_user_service)


from dotenv import load_dotenv

env_file = os.getenv('ENV_FILE', '.env.dev')
load_dotenv(env_file)

print(f"ENV_FILE: {env_file}")

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'response': 'ok'})

@app.route('/user', methods=['GET'])
def get_users():
    users, error, status_code = get_all_users_service()
    if error:
        return jsonify({'message': f'Error retrieving users: {error}'}), status_code
    return jsonify(users)

@app.route('/user/<int:uid>', methods=['GET'])
def get_user(uid):
    user, error, status_code = get_user_service(uid)
    if error:
        return jsonify({'message': error}), status_code
    return jsonify(user)

@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    
    error_message, valid, status_code = validate_user_input_service(data)
    if not valid:
        return jsonify({'message': error_message}), status_code

    name = data.get('name')
    age = data.get('age')

    response_data, error, status_code = add_user_service(name, age)
    if error:
        return jsonify({'message': f'Error adding user: {error}'}), status_code
    return jsonify(response_data), status_code

@app.route('/user/<int:uid>', methods=['PATCH'])
def update_user(uid):
    data = request.get_json()
    
    user, error, status_code = get_user_service(uid)
    if error:
        return jsonify({'message': error}), status_code


    response_data, error, status_code = update_user_service(uid, name=data.get('name'), age=data.get('age'))
    if error:
        return jsonify({'message': f'Error updating user: {error}'}), status_code
    else:
        return jsonify(response_data), status_code

@app.route('/user/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    user, error, status_code = get_user_service(uid)
    if error:
        return jsonify({'message': error}), status_code

    response_data, error, status_code = delete_user_service(uid)
    if error:
        return jsonify({'message': f'Error deleting user: {error}'}), status_code
    return jsonify(response_data), status_code

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    print("port", port)
    env = os.getenv('FLASK_ENV', 'development')
    app.run(host='0.0.0.0', port=port, debug=env == 'development')
