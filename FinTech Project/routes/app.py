from flask import Blueprint, request, render_template, jsonify, session, redirect, Flask, url_for
import database

# Define the Blueprint
auth_bp = Blueprint('auth', __name__)

# Authentication routes
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
from flask import Flask, request, redirect, url_for, jsonify

app = Flask(__name__)


@app.route('/artist-producer-information', methods=['POST'])
def create_artist_account():
    # Extract form data
    data = request.get_json()
    username = data.get('username')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    role = 'artist'

    # Validate data (pseudo-code)
    if not username or not firstname or not lastname or not email:
        return jsonify({"message": "All fields are required."}), 400

    # Save artist account to the database (pseudo-code)
    # db.save_artist(username, firstname, lastname, email)

    # Return success response
    
    try:
        # Register the user in the database
        database.register_user(username, firstname, lastname, email, role)
        return jsonify({'message': 'User registered successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/artist-landing-page')
def artist_landing_page():
    return "Welcome to the Artist Landing Page!"

if __name__ == '__main__':
    app.run(debug=True)
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

# Define the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management
app.register_blueprint(auth_bp)

# Buy share route
@app.route('/api/buy_share', methods=['POST'])
def buy_share():
    data = request.json
    investor_id = data.get('investor_id')
    music_id = data.get('music_id')
    shares_to_buy = data.get('shares_to_buy')

    if not investor_id or not music_id or not shares_to_buy:
        return jsonify({'error': 'Missing required fields.'}), 400

    music_share = database.get_music_share(music_id)
    if not music_share:
        return jsonify({'error': 'Music share not found.'}), 404

    if music_share['available_shares'] < shares_to_buy:
        return jsonify({'error': 'Not enough shares available.'}), 400

    total_cost = shares_to_buy * music_share['price_per_share']

    investor = database.get_user(investor_id)
    if not investor:
        return jsonify({'error': 'Investor not found.'}), 404

    if investor['balance'] < total_cost:
        return jsonify({'error': 'Insufficient balance.'}), 400

    new_balance = investor['balance'] - total_cost
    database.update_user_balance(investor_id, new_balance)

    new_available_shares = music_share['available_shares'] - shares_to_buy
    database.update_music_share_availability(music_id, new_available_shares)

    database.save_transaction(investor_id, music_id, shares_to_buy, total_cost)

    return jsonify({'message': 'Share purchased successfully!'})

# List music share route
@app.route('/api/list_share', methods=['POST'])
def list_share():
    data = request.json
    artist_id = data['artist_id']
    music_id = data['music_id']
    total_shares = data['total_shares']
    price_per_share = data['price_per_share']

    database.list_music_shares(artist_id, music_id, total_shares, price_per_share)

    return jsonify({'message': 'Music share listed successfully!'})

# Create song route
@app.route('/create_song', methods=['POST'])
def create_song():
    data = request.json
    title = data['title']
    artist = data['artist']
    total_shares = data['total_shares']
    price_per_share = data['price_per_share']

    try:
        database.create_song(title, artist, total_shares, price_per_share)
        return jsonify({"message": "Song created successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Distribute revenue route
@app.route('/distribute_revenue', methods=['POST'])
def distribute_revenue():
    data = request.json
    song_id = data['song_id']

    try:
        database.distribute_revenue(song_id)
        return jsonify({"message": "Revenue distributed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Helper function to fetch a song
def get_song(song_id):
    return database.get_song(song_id)

@app.route('/api/songs', methods=['GET'])
def get_songs():
    try:
        # Fetch all songs from the database
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM music_shares')
        songs = cursor.fetchall()
        conn.close()

        # Convert the songs to a list of dictionaries
        songs_list = []
        for song in songs:
            songs_list.append({
                'id': song['id'],
                'title': song['music_id'],  # Assuming 'music_id' is the song title
                'available_shares': song['available_shares'],
                'price_per_share': song['price_per_share']
            })

        return jsonify(songs_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/artist/<username>')
def artist_profile(username):
    try:
        # Fetch artist data from the database
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM artists WHERE username = ?', (username,))
        artist = cursor.fetchone()
        conn.close()

        if artist:
            # Render the artist profile template with the fetched data
            return render_template('artist-landing-page.html', 
                                  artist_name=artist['name'],
                                  genre=artist['genre'],
                                  bio=artist['bio'],
                                  share_value=artist['share_value'],
                                  available_shares=artist['available_shares'],
                                  top100=artist['top100'],
                                  top200=artist['top200'])
        else:
            return "Artist not found.", 404
    except Exception as e:
        return str(e), 500
if __name__ == '__main__':
    app.run(debug=True)
