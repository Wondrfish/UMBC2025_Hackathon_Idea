from flask import Flask, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Instanstiaze flask app
app = Flask(__name__)

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


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


# class UserActivity(db.Model):
#     """
#     Model for user activity points (how much profit, trades, etc.)
#     """


if __name__ == "__main__":
    app.run(debug=True)
