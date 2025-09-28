from flask import Flask, jsonify
import os
import sys
import pandas as pd
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


# ===================
# DB Models
# ===================
class Youtuber(db.Model):
    """
    Model for Youtuber "stock" selection
    """

    __tablename__ = "youtube_channels"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)  # primary key
    channel_name = db.Column(db.String(100), unique=True, nullable=False)
    channel_handle = db.Column(db.String(100), unique=True, nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True)
    view_count = db.Column(db.Integer, nullable=False)
    subs = db.Column(db.Integer, nullable=False)


class UserBehavior(db.Model):
    """
    Model for user activity points (how much profit, trades, etc.)
    """

    __tablename__ = "user_behavior"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)  # primary key
    day = db.Column(db.Integer, nullable=False)
    bought_stocks = db.Column(
        db.Integer, db.ForeignKey("youtube_channels.id"), nullable=False
    )
    sold_stocks = db.Column(
        db.Integer, db.ForeignKey("youtube_channels.id"), nullable=False
    )
    running_net = db.Column(db.Integer)


# -------------------------
# Create tables (if not exist)
# -------------------------
with app.app_context():
    db.create_all()
    print("Database file created at:", os.path.abspath("db.sqlite3"))


# with app.app_context():
#     db.drop_all()  # deletes all tables
#     db.create_all()  # recreate tables


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
    handles = parse_handles()
    for item in handles:
        youtube = get_youtube_service_api_key()
        request = youtube.channels().list(part="snippet, statistics", forHandle=item)
        response = request.execute()

        if response:

            print(f"{item} Channel Info (API Key):")
            # print(response)

            channel_items = response["items"]
            channel = response["items"][0]

            channel_name = channel["snippet"]["title"]
            channel_pic = channel["snippet"]["thumbnails"]["default"]["url"]
            stats = channel["statistics"]

            # Print or return
            print("Channel Name:", channel_name)
            # print("Channel Pic URL:", channel_pic)
            # print("Channel info:", response["items"])
            print("Statistics:", stats)

            new_channel = Youtuber(
                channel_name=channel_name,
                channel_handle=channel["snippet"]["customUrl"],
                profile_pic=channel_pic,
                view_count=int(stats["viewCount"]),
                subs=int(stats["subscriberCount"]),
            )

            db.session.add(new_channel)
            db.session.commit()


def get_youtube_service_api_key():
    """Create a YouTube API service using an API key."""
    return googleapiclient.discovery.build("youtube", "v3", developerKey=YT_API_KEY)


def parse_handles():

    # Load CSV into a DataFrame
    df = pd.read_csv(
        "../popular_channel_handles.txt",
        delimiter=",",  # custom delimiter (default is ",")
        header=0,  # row number to use as column names
        skiprows=1,  # skip first row(s)
        names=["channel", "handle", "relation"],  # custom column names
        usecols=[0, 1],  # read only certain columns
        na_values=["NA", ""],  # treat these as missing values
    )

    handles = df["handle"].tolist()
    print(handles)
    return handles


if __name__ == "__main__":
    app.run(debug=True)
