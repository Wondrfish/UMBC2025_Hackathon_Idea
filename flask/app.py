from flask import Flask, jsonify
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Instanstiaze flask app
app = Flask(__name__)

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

YT_API_KEY = os.getenv("YOUTUBE_API_KEY")
PUBLIC_CHANNEL_ID = "@GoogleDevelopers"


@app.route("/")
def home():
    return "Hello world!"


@app.route("/analyze/")
def analyze():
    """
    View to grab data points from db and analyze money loss patterns.
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    # Pass context text + user data into gemini to analyze user behavior
    response = model.generate_content(grab_context())
    # print(response.text)
    return f"{response.text[:100]}..."


def grab_context():
    """
    Grabs context points from db and formats them into a text file to feed to Gemini.
    """
    # The explanation part of the prompt
    CONTEXT_TEXT = "The following data contains information on fictional stockmarket trades using \
        data from YouTube instead of stocks. Analyze the data points and give a warm but encouraging \
            critique on what the user could have done differently while educating them on the follwing \
                topics: Portfolio Management: Goal setting, rebalancing, risk tolerance, long-term and \
                    the understanding and application of key investing principles"
    # Pull user data from db and parse into strings
    user_data = " "
    return f"{CONTEXT_TEXT}\n {user_data}"


@app.route("/grab-yt-data/")
def grab_yt_data():
    get_public_channel_info()
    return "hi"


# -----------------------------
# API REQUEST FUNCTIONS
# -----------------------------
def get_public_channel_info():
    """Retrieve info about a public channel using an API key."""
    youtube = get_youtube_service_api_key()
    request = youtube.channels().list(
        part="snippet, statistics", forHandle=PUBLIC_CHANNEL_ID
    )
    response = request.execute()

    print(f"{PUBLIC_CHANNEL_ID} Channel Info (API Key):")
    # print(response)

    channel = response["items"][0]

    channel_name = channel["snippet"]["title"]
    channel_pic = channel["snippet"]["thumbnails"]["default"]["url"]
    stats = channel["statistics"]

    # Print or return
    print("Channel Name:", channel_name)
    print("Channel Pic URL:", channel_pic)
    print("Statistics:", stats)


def get_youtube_service_api_key():
    """Create a YouTube API service using an API key."""
    return googleapiclient.discovery.build("youtube", "v3", developerKey=YT_API_KEY)


# class UserActivity(db.Model):
#     """
#     Model for user activity points (how much profit, trades, etc.)
#     """


if __name__ == "__main__":
    app.run(debug=True)
