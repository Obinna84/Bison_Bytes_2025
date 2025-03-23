from flask import Blueprint, request, jsonify, session, redirect, url_for
import database

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    role = data['role']

    try:
        database.register_user(username, firstname, lastname, email, role)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'message': 'User registered successfully!'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = database.authenticate_user(username, password)
    if user:
        session['firstname'] = user['firstname']
        return jsonify({'message': 'Logged in successfully!'})
    return jsonify({'error': 'Invalid credentials.'}), 401

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login_page'))