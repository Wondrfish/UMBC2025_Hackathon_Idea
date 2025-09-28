from flask import Flask, jsonify
import os
import sys
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from typing import Dict, List, Tuple
import math
import random
import statistics

# import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Instanstiaze flask app
app = Flask(__name__)

from flask_cors import CORS

CORS(app)


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
    __tablename__ = "youtube_channels"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(100), unique=True, nullable=False)
    channel_handle = db.Column(db.String(100), unique=True, nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True)
    view_count = db.Column(db.Integer, nullable=False)

    # one-to-many
    stats = db.relationship(
        "ChannelStats", back_populates="youtuber", cascade="all, delete-orphan"
    )


class ChannelStats(db.Model):
    __tablename__ = "channel_stats"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    youtuber_id = db.Column(
        db.Integer, db.ForeignKey("youtube_channels.id"), nullable=False
    )
    day = db.Column(db.Integer)
    view_count = db.Column(db.Integer, nullable=False)

    # back reference matches exactly
    youtuber = db.relationship("Youtuber", back_populates="stats")


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
            )

            db.session.add(new_channel)
            db.session.commit()


@app.route("/get-yt-channels-and-views/")
def get_yt_channels_and_views():
    channels = Youtuber.query.all()
    channel_list = [{"name": c.channel_name, "views": c.view_count} for c in channels]
    return jsonify(channel_list)


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


@app.route("/calculate-weekly-price/")
def calculate_weekly_price():
    # grab each stock from db
    # Example: turn Youtuber.channel_name -> Youtuber.subs into a dict
    channels = Youtuber.query.all()
    channel_dict = {c.channel_name: c.view_count for c in channels}
    channel_new_dict = {c.channel_name: c.view_count for c in channels}

    # print(channel_dict)

    for channel in channel_dict:
        channel_new_dict[channel] = int(
            map_stats_to_price_and_vol(channel_dict[channel]) * channel_dict[channel]
        )

        print(f"{channel}: {channel_dict[channel]} -> {channel_new_dict[channel]}")

    return channel_new_dict


@app.route("/populate-historical-data/")
def populate_historical_data():
    i = 1
    historical_data = calculate_weekly_price()
    for i in range(7):
        for channel in historical_data:
            if Youtuber.query.filter_by(channel_name=channel).first() is not None:
                r = random.uniform(0, 10)
                vol = 1 + (r / 10)
                new_stat = ChannelStats(
                    youtuber_id=Youtuber.query.filter_by(channel_name=channel)
                    .first()
                    .id,
                    day=i,
                    view_count=int(historical_data[channel] * vol),
                )
                db.session.add(new_stat)
                db.session.commit()

    return "hi"


def _seed(seed: int):
    random.seed(seed)


def map_stats_to_price_and_vol(viewCount):
    """Map channel stats to an initial price and daily volatility.

    Input:
    Heuristics used:
    - initial price scales with sqrt(subscribers) to dampen extremes
    - volatility inversely scales with log(views+1) so larger channels are slightly less volatile

    Args:
        'viewCount'

    Returns:
        (initial_price, daily_volatility)
        # vol = ex: 1.12 mean a 12% increase
    """
    views = viewCount if viewCount else 1000000  # Set default to 1,000,000 views

    # avoid zero/negative
    views = max(views, 1)

    # volatility heuristic (daily stddev)
    vol = 0.02 + 0.08 / (math.log(views + 10) + 1)

    print("vol:", vol)
    return 1 + float(vol)


# def generate_price_series(
#     stats: Dict[str, int],
#     days: int = 90,
#     seed: int = 42,
#     drift: float = 0.0005,
# ) -> List[float]:
#     """Generate a synthetic daily price series for a single channel.

#     Uses a simple geometric random walk: S_t+1 = S_t * exp((mu - 0.5*sigma^2) + sigma * Z)
#     where Z ~ N(0,1).

#     Args:
#         stats: channel stats dict with subscriberCount and viewCount
#         days: number of days to simulate
#         seed: RNG seed for reproducibility
#         drift: base daily drift applied to all channels (can be positive/negative)

#     Returns:
#         list of daily prices, length = days
#     """
#     _seed(seed)
#     s0, sigma = map_stats_to_price_and_vol(stats)
#     prices = [s0]
#     for _ in range(days - 1):
#         # sample Z from standard normal
#         z = random.gauss(0, 1)
#         ret = (drift - 0.5 * sigma * sigma) + sigma * z
#         next_price = max(0.01, prices[-1] * math.exp(ret))
#         prices.append(next_price)
#     return prices


# def generate_stats_time_series(
#     base_stats: Dict[str, int], days: int = 90, seed: int = 42
# ) -> List[Dict[str, int]]:
#     """Generate a per-day time series of statistics (subscriberCount, viewCount).

#     The generator uses a small positive drift with gaussian noise so counts slowly
#     grow (or fluctuate) over time. Returns a list of dicts for each day.
#     """
#     _seed(seed)
#     subs0 = int(base_stats.get("subscriberCount", 1000))
#     views0 = int(base_stats.get("viewCount", 10000))

#     subs0 = max(1, subs0)
#     views0 = max(1, views0)

#     series = []
#     subs = subs0
#     views = views0
#     for _ in range(days):
#         # small percent changes
#         subs_change = random.gauss(0.0008, 0.005)  # mean growth ~0.08% daily
#         views_change = random.gauss(0.001, 0.02)

#         subs = max(0, int(subs * (1 + subs_change)))
#         views = max(0, int(views * (1 + views_change)))

#         series.append({"subscriberCount": subs, "viewCount": views})

#     return series


# def simulate_portfolio(
#     channels: List[Dict],
#     days: int = 7,
#     seed: int = 42,
#     allocation: Dict[str, float] = None,
# ) -> Dict:
#     """Simulate a simple buy-and-hold portfolio across multiple channels.

#     Each channel dict should include at least 'channel_name' and 'statistics'.

#     Args:
#         channels: list of channel dicts
#         days: number of days to simulate
#         seed: RNG seed
#         allocation: optional dict mapping channel_name to fraction (sums to 1). If not
#             provided, channels are equally weighted.

#     Returns:
#         dict with per-channel price series and portfolio value series
#     """
#     _seed(seed)
#     n = len(channels)
#     if n == 0:
#         return {"portfolio": [], "channels": {}}

#     if allocation is None:
#         # equal weight
#         weight = 1.0 / n
#         allocation = {
#             c.get("channel_name", f"ch{i}"): weight for i, c in enumerate(channels)
#         }

#     channel_prices = {}
#     for i, ch in enumerate(channels):
#         name = ch.get("channel_name", f"ch{i}")
#         stats = ch.get("statistics", {})
#         # derive a per-channel seed to keep reproducible but different
#         ch_seed = seed + i * 100
#         prices = generate_price_series(stats, days=days, seed=ch_seed)
#         channel_prices[name] = prices

#     # Build portfolio value series assuming $1 starting capital
#     # buy proportional shares at day 0
#     initial_capital = 500.0
#     shares = {}
#     for name, prices in channel_prices.items():
#         w = allocation.get(name, 0.0)
#         # dollar allocation
#         dollars = initial_capital * w
#         shares[name] = dollars / prices[0] if prices[0] > 0 else 0.0

#     portfolio = []
#     for day in range(days):
#         total = 0.0
#         for name, prices in channel_prices.items():
#             total += shares[name] * prices[day]
#         portfolio.append(total)

#     return {
#         "channels": channel_prices,
#         "portfolio": portfolio,
#         "allocation": allocation,
#     }


# def summarize_portfolio(portfolio_values: List[float]) -> Dict[str, float]:
#     """Return simple summary metrics for a portfolio value series."""
#     if not portfolio_values:
#         return {}
#     start = portfolio_values[0]
#     end = portfolio_values[-1]
#     ret = (end / start) - 1.0 if start else 0.0
#     daily_rets = [
#         (portfolio_values[i + 1] / portfolio_values[i]) - 1
#         for i in range(len(portfolio_values) - 1)
#         if portfolio_values[i] > 0
#     ]
#     vol = statistics.pstdev(daily_rets) if daily_rets else 0.0
#     return {"start": start, "end": end, "return": ret, "daily_vol": vol}


if __name__ == "__main__":
    app.run(debug=True)
