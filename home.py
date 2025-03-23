from flask import Flask, redirect, request, jsonify, session, render_template
import json
import os

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
        return render_template("Home.html",user_name="guest",pfp="static/guest_pfp.png")
    
@app.route("/artist-producer-information", methods=['GET','POST'])
def send_to_homepage():
    acceptable_img_files = [".png",".jpg"]
    artist_producer_json_info = request.form
    user_name = artist_producer_json_info["username"]
    user_first_name = artist_producer_json_info["firstname"]
    user_last_name = artist_producer_json_info["lastname"]
    user_email = artist_producer_json_info["email"]
    #profile_picture = artist_producer_json_info["user-pfp"]
    return render_template("Home.html",email=user_email,user_name=user_name,fname=user_first_name,lname=user_last_name,pfp=profile_picture)

@app.route("/Marketplace.html")
def load_marketplace_page():
    return render_template("Marketplace.html",pfp=profile_picture)

@app.route("/Home.html")
def load_home_page():
    return render_template("Home.html",pfp=profile_picture)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
