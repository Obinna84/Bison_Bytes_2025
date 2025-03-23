from flask import Flask, redirect, request, jsonify, session, render_template
import json
import os
import api

app = Flask(__name__)

profile_picture = "static/guest_pfp.png"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/user-type-selected", methods=['GET','POST'])
def handle_user_type():
    user_type_form = request.form
    user_type = user_type_form["user-type"]
    if user_type == "artist/producer":
        return render_template("artist-registration-page.html")
    if user_type == "fan/investor":
        return render_template("investor-listener-registration-page.html")
    if user_type == "guest":
        return render_template("Home.html", user_name="guest", pfp=profile_picture)
    
@app.route("/artist-producer-information", methods=['GET','POST'])
def send_to_homepage():
    acceptable_img_files = [".png",".jpg"]
    artist_producer_json_info = request.form
    user_name = artist_producer_json_info["username"]
    user_first_name = artist_producer_json_info["firstname"]
    user_last_name = artist_producer_json_info["lastname"]
    user_email = artist_producer_json_info["email"]
    #profile_picture = artist_producer_json_info["user-pfp"]
    return render_template("Home.html", email=user_email, user_name=user_name, fname=user_first_name, lname=user_last_name, pfp=profile_picture)

@app.route("/Marketplace.html")
def load_marketplace_page():
    return render_template("Marketplace.html", pfp=profile_picture)

@app.route("/Profile.html")
def load_profile_page():
    return render_template("pr.html", pfp=profile_picture)

@app.route("/Home.html")
def load_home_page():
    return render_template("Home.html", pfp=profile_picture)

@app.route("/search_results", methods=['GET', 'POST'])
def load_search_results():
    # Placeholder data for testing
    info = {
        "recommended_artists": ["Artist 1", "Artist 2"],
        "recommended_artists_images": ["image1.jpg", "image2.jpg"]
    }
    recommended_artists_data = zip(info["recommended_artists"], info["recommended_artists_images"])
    return render_template("search_result.html", pfp=profile_picture, recommended_artists_data=recommended_artists_data, **info)

# Sample data for demonstration
artist_data = {
    "Bruno Mars": {
        "genre": "Pop, Funk, R&B",
        "bio": "Bruno Mars is an American singer, songwriter, and record producer.",
        "share_value": "$XYZ",
        "available_shares": "1000",
        "top100": "7",
        "top200": "2"
    },
    "Earl Sweatshirt": {
        "genre": "Hip-Hop, Rap",
        "bio": "Earl Sweatshirt is an American rapper and songwriter.",
        "share_value": "$ABC",
        "available_shares": "850",
        "top100": "0",
        "top200": "0"
    },
    "MIKE": {
        "genre": "Underground Hip-Hop",
        "bio": "MIKE is a rapper known for his introspective lyrics.",
        "share_value": "$DEF",
        "available_shares": "720",
        "top100": "3",
        "top200": "1"
    },
    "Solange": {
        "bio": "Solange is an American singer, songwriter, and record producer.",
        "share_value": "$GHI",
        "available_shares": "72",
        "top100": "5",
        "top200": "0"
    }
}

@app.route('/artist/<artist_name>')
def artist_landing(artist_name):
    artist_info = artist_data.get(artist_name, None)
    if not artist_info:
        return "Artist not found", 404
    return render_template('artist-landing-page.html', artist_name=artist_name, **artist_info)

@app.route('/community.html')
def load_community_tab():
    return render_template("community.html", pfp=profile_picture)

@app.route('/Purchase.html')
def load_purchase_tab():
    return render_template('Purchase.html', pfp=profile_picture)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)