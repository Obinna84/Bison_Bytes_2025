import unittest
from unittest.mock import patch
from flask import Flask, session
from flask.testing import FlaskClient
from auth import auth_bp, database  # Replace 'your_application' with the actual module name


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test Flask application
        self.app = Flask(__name__)
        self.app.register_blueprint(auth_bp)
        self.app.secret_key = 'test_secret_key'  # Required for session handling

        # Set up a test client
        self.client = self.app.test_client()

    @patch('database.register_user')
    def test_register_success(self, mock_register_user):
        # Mock the database.register_user method
        mock_register_user.return_value = None

        # Test data
        data = {
            'username': 'testuser',
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test@example.com',
            'role': 'user'
        }

        # Make a POST request to the /register endpoint
        response = self.client.post('/register', json=data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'User registered successfully!'})

    @patch('database.register_user')
    def test_register_failure(self, mock_register_user):
        # Mock the database.register_user method to raise an exception
        mock_register_user.side_effect = Exception('Database error')

        # Test data
        data = {
            'username': 'testuser',
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test@example.com',
            'role': 'user'
        }

        # Make a POST request to the /register endpoint
        response = self.client.post('/register', json=data)

        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Database error'})

    @patch('database.authenticate_user')
    def test_login_success(self, mock_authenticate_user):
        # Mock the database.authenticate_user method
        mock_authenticate_user.return_value = {
            'firstname': 'Test'
        }

        # Test data
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        # Make a POST request to the /login endpoint
        response = self.client.post('/login', json=data)

        # Assert the response and session
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Logged in successfully!'})
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['firstname'], 'Test')

    @patch('database.authenticate_user')
    def test_login_failure(self, mock_authenticate_user):
        # Mock the database.authenticate_user method to return None
        mock_authenticate_user.return_value = None

        # Test data
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

        # Make a POST request to the /login endpoint
        response = self.client.post('/login', json=data)

        # Assert the response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {'error': 'Invalid credentials.'})

def test_register_missing_fields(self):
    # Test data with missing 'username'
        data = {
            'firstname': 'Test',
         'lastname': 'User',
         'email': 'test@example.com',
         'role': 'user'
      }

    # Make a POST request to the /register endpoint
        response = self.client.post('/register', json=data)

    # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

def test_login_missing_fields(self):
    # Test data with missing 'password'
        data = {
        'username': 'testuser'
        }

    # Make a POST request to the /login endpoint
        response = self.client.post('/login', json=data)

    # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)