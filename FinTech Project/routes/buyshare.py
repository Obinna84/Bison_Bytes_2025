from flask import Flask, request, jsonify
import database  # Your database module

app = Flask(__name__)

@app.route('/api/buy_share', methods=['POST'])
def buy_share():
    # Get data from the request
    data = request.json
    investor_id = data.get('investor_id')
    music_id = data.get('music_id')
    shares_to_buy = data.get('shares_to_buy')

    # Validate required fields
    if not investor_id or not music_id or not shares_to_buy:
        return jsonify({'error': 'Missing required fields.'}), 400

    # Fetch the music share details
    music_share = database.get_music_share(music_id)
    if not music_share:
        return jsonify({'error': 'Music share not found.'}), 404

    # Check if enough shares are available
    if music_share['available_shares'] < shares_to_buy:
        return jsonify({'error': 'Not enough shares available.'}), 400

    # Calculate total cost
    total_cost = shares_to_buy * music_share['price_per_share']

    # Fetch the investor's details
    investor = database.get_user(investor_id)
    if not investor:
        return jsonify({'error': 'Investor not found.'}), 404

    # Check if the investor has enough balance
    if investor['balance'] < total_cost:
        return jsonify({'error': 'Insufficient balance.'}), 400

    # Deduct balance from the investor
    new_balance = investor['balance'] - total_cost
    database.update_user_balance(investor_id, new_balance)

    # Update the music share availability
    new_available_shares = music_share['available_shares'] - shares_to_buy
    database.update_music_share_availability(music_id, new_available_shares)

    # Record the transaction
    database.save_transaction(investor_id, music_id, shares_to_buy, total_cost)

    return jsonify({'message': 'Share purchased successfully!'})

if __name__ == '__main__':
    app.run(debug=True)