from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

# Instanstiaze flask app
app = Flask(__name__)

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

load_dotenv()


@app.route("/")
def home():
    parse_handles()
    return "Hello world!"


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

    # Show first 5 rows
    # print(df.head())

    handles = df["handle"].tolist()
    print(handles)


if __name__ == "__main__":
    app.run(debug=True)
