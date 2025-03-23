import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('music_shares.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database (run this once)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        genre TEXT,
        bio TEXT,
        share_value REAL DEFAULT 0.0,
        available_shares INTEGER DEFAULT 0,
        top100 TEXT,
        top200 TEXT
    );
    ''')
    
    # Create music_shares table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS music_shares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            music_id TEXT NOT NULL,
            artist_id INTEGER NOT NULL,
            total_shares INTEGER NOT NULL,
            available_shares INTEGER NOT NULL,
            price_per_share REAL NOT NULL,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (artist_id) REFERENCES users (id)
        )
    ''')

    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            investor_id INTEGER NOT NULL,
            music_id TEXT NOT NULL,
            shares_bought INTEGER NOT NULL,
            total_cost REAL NOT NULL,
            timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (investor_id) REFERENCES users (id),
            FOREIGN KEY (music_id) REFERENCES music_shares (music_id)
        )
    ''')

    # Create songs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            total_shares INTEGER NOT NULL,
            shares_available INTEGER NOT NULL,
            price_per_share REAL NOT NULL,
            revenue REAL DEFAULT 0.0
        )
    ''')

    # Create shareholders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shareholders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            song_id INTEGER NOT NULL,
            num_shares INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (song_id) REFERENCES songs (id)
        )
    ''')

    # Create revenue_distributions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS revenue_distributions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (song_id) REFERENCES songs (id)
        )
    ''')

    conn.commit()
    conn.close()

# Register a new user
def register_user(username, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        raise ValueError(f"Username '{username}' already exists. Please choose a different username.")

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    # Insert the new user into the database
    cursor.execute('''
        INSERT INTO users (username, password, role, balance)
        VALUES (?, ?, ?, ?)
    ''', (username, hashed_password, role, 0.0))

    conn.commit()
    conn.close()
def add_artist(username, name, genre, bio, share_value, available_shares, top100, top200):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO artists (username, name, genre, bio, share_value, available_shares, top100, top200)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, name, genre, bio, share_value, available_shares, top100, top200))
    conn.commit()
    conn.close()
def get_artist(artist_id):
    """
    Fetch an artist's details from the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT *
        FROM artists
        WHERE id = ?
    ''', (artist_id,))
    artist = cursor.fetchone()
    conn.close()
    return artist

def calculate_artist_share_value(artist_id):
    """
    Calculate the average share value for an artist based on their listed songs.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all songs by the artist
    cursor.execute('''
        SELECT price_per_share, total_shares
        FROM music_shares
        WHERE artist_id = ?
    ''', (artist_id,))
    songs = cursor.fetchall()

    conn.close()

    if not songs:
        return 0.0  # Default value if no songs are listed

    # Calculate the weighted average share value
    total_value = sum(song['price_per_share'] * song['total_shares'] for song in songs)
    total_shares = sum(song['total_shares'] for song in songs)

    if total_shares == 0:
        return 0.0  # Avoid division by zero

    return total_value / total_shares


def calculate_artist_available_shares(artist_id):
    """
    Calculate the total available shares for an artist based on their listed songs.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all songs by the artist
    cursor.execute('''
        SELECT available_shares
        FROM music_shares
        WHERE artist_id = ?
    ''', (artist_id,))
    songs = cursor.fetchall()

    conn.close()

    if not songs:
        return 0  # Default value if no songs are listed

    # Sum up the available shares
    return sum(song['available_shares'] for song in songs)


def update_artist_shares(artist_id):
    """
    Update the artist's share_value and available_shares in the artists table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Calculate the average share value and available shares
    share_value = calculate_artist_share_value(artist_id)
    available_shares = calculate_artist_available_shares(artist_id)

    # Update the artist's record
    cursor.execute('''
        UPDATE artists
        SET share_value = ?, available_shares = ?
        WHERE id = ?
    ''', (share_value, available_shares, artist_id))

    conn.commit()
    conn.close()
# Authenticate a user
def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the user from the database
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()

    # Verify the password
    if user and check_password_hash(user['password'], password):
        return user
    return None

# Get user by username
def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_music_share(music_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM music_shares WHERE music_id = ?', (music_id,))
    music_share = cursor.fetchone()
    conn.close()
    return music_share


def update_user_balance(user_id, new_balance):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
    conn.commit()
    conn.close()

def update_music_share_availability(music_id, new_available_shares):
    conn = get_db_connection()
    cursor =conn.cursor()
    cursor.execute('UPDATE music_shares SET available_shares = ? WHERE music_id = ?', (new_available_shares, music_id))
    conn.commit()
    conn.close()

def list_music_shares(artist_id, music_id, total_shares, price_per_share):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO music_shares (artist_id, music_id, total_shares, available_shares, price_per_share)
        VALUES (?, ?, ?, ?, ?)
    ''', (artist_id, music_id, total_shares, total_shares, price_per_share))
    conn.commit()
    conn.close()

    # Update the artist's share value and available shares
    update_artist_shares(artist_id)

def save_transaction(investor_id, music_id, shares_bought, total_cost):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (investor_id, music_id, shares_bought, total_cost)
        VALUES (?, ?, ?, ?)
    ''', (investor_id, music_id, shares_bought, total_cost))
    conn.commit()
    conn.close()

def create_song(title, artist, total_shares, price_per_share):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO songs (title, artist, total_shares, shares_available, price_per_share)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, artist, total_shares, total_shares, price_per_share))
    conn.commit()
    conn.close()

def get_song(song_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM songs WHERE id = ?', (song_id,))
    song = cursor.fetchone()
    conn.close()
    return song

def update_song_revenue(song_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE songs SET revenue = revenue + ? WHERE id = ?', (amount, song_id))
    conn.commit()
    conn.close()

def distribute_revenue(song_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the song and its shareholders
    cursor.execute('SELECT * FROM songs WHERE id = ?', (song_id,))
    song = cursor.fetchone()
    cursor.execute('SELECT * FROM shareholders WHERE song_id = ?', (song_id,))
    shareholders = cursor.fetchall()

    # Distribute revenue to each shareholder
    for shareholder in shareholders:
        user_id = shareholder['user_id']
        num_shares = shareholder['num_shares']
        amount = (num_shares / song['total_shares']) * song['revenue']
        cursor.execute('UPDATE users SET balance = balance + ? WHERE id = ?', (amount, user_id))

    # Reset the song's revenue
    cursor.execute('UPDATE songs SET revenue = 0 WHERE id = ?', (song_id,))

    # Record the revenue distribution
    cursor.execute('''
        INSERT INTO revenue_distributions (song_id, amount)
        VALUES (?, ?)
    ''', (song_id, song['revenue']))

    conn.commit()
    conn.close()
# Initialize the database (run this once)
if __name__ == '__main__':
    init_db()
    add_artist(
    username='kendrick_lamar',
    name='Kendrick Lamar',
    genre='Rap',
    bio='Kendrick Lamar Duckworth (born June 17, 1987) is an American rapper. Regarded as one of the greatest rappers of all time.',
    share_value=560.0,
    available_shares=1000,
    top100='HUMBLE., DNA., Alright, Money Trees, Swimming Pools (Drank)',
    top200='good kid, m.A.A.d city, To Pimp a Butterfly, DAMN., Mr. Morale & the Big Steppers'
)