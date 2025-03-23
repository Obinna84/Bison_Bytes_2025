from flask import Flask, request, jsonify
import database  # Your database module

app = Flask(__name__)

@app.route('/api/list_share', methods=['POST'])
def list_share():
    data = request.json
    artist_id = data['artist_id']
    music_id = data['music_id']
    total_shares = data['total_shares']
    price_per_share = data['price_per_share']

    # Save the new music share to the database
    database.list_music_shares(artist_id, music_id, total_shares, price_per_share)

    return jsonify({'message': 'Music share listed successfully!'})

if __name__ == '__main__':
    app.run(debug=True)