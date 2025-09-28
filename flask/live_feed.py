import time
import os
import googleapiclient.discovery
from dotenv import load_dotenv
import threading
from typing import List

load_dotenv()
YT_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Default handles file (repo root, relative to this module)
HANDLES_FILE = os.path.join(os.path.dirname(__file__), "..", "popular_channel_handles.txt")


def get_channel_info_by_handle(handle: str):
    """Call YouTube API channels.list for a handle and return a simplified dict.

    Returns None on error or missing API key.
    """
    if not YT_API_KEY:
        print("No YOUTUBE_API_KEY found in environment; cannot fetch live data.")
        return None
    # build client once per call
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YT_API_KEY)

    # Try multiple strategies to resolve a handle/name to channel information.
    attempts = [
        {"params": {"part": "snippet,statistics", "forHandle": handle}},
        {"params": {"part": "snippet,statistics", "forUsername": handle}},
    ]

    # perform attempts with short retry on transient errors
    for attempt in attempts:
        try:
            req = youtube.channels().list(**attempt["params"])
            res = req.execute()
            items = res.get("items", [])
            if items:
                c = items[0]
                return {"channel_name": c["snippet"]["title"], "statistics": c["statistics"]}
        except Exception as e:
            # transient error — try next strategy
            print(f"YouTube API attempt failed ({attempt['params'].keys()}):", e)

    # Fallback: search by query to find likely channel id, then fetch by id
    try:
        sreq = youtube.search().list(part="snippet", q=handle, type="channel", maxResults=1)
        sres = sreq.execute()
        items = sres.get("items", [])
        if items:
            channel_id = items[0]["snippet"]["channelId"]
            creq = youtube.channels().list(part="snippet,statistics", id=channel_id)
            cres = creq.execute()
            citems = cres.get("items", [])
            if citems:
                c = citems[0]
                return {"channel_name": c["snippet"]["title"], "statistics": c["statistics"]}
    except Exception as e:
        print("YouTube search fallback failed:", e)

    return None


def live_feed(handle: str, interval: int = 45):
    """Continuously print live stats for a channel every `interval` seconds."""
    try:
        while True:
            data = get_channel_info_by_handle(handle)
            if data:
                stats = data["statistics"]
                subs = stats.get("subscriberCount")
                views = stats.get("viewCount")
                print(f"{data['channel_name']} | Subs: {subs} | Views: {views}")
            else:
                print("Error fetching data or no API key.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Live feed stopped by user.")


def load_handles(file_path: str = HANDLES_FILE) -> List[str]:
    """Load handles from a CSV-like file. Returns list of handle strings.

    The file format is expected to have a header like `Channel,Handle / URL name,Notes`.
    We parse each non-empty line, skip fences, and return the second column when present.
    """
    handles = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("```"):
                    continue
                # skip header
                if line.lower().startswith("channel,handle"):
                    continue
                parts = line.split(",", 2)
                if len(parts) >= 2:
                    handle = parts[1].strip()
                else:
                    handle = parts[0].strip()
                # sanitize handle: strip quotes and whitespace
                if handle:
                    handle = handle.strip().strip('"').strip("'")
                    # For API, allow both with and without leading @. Keep as-is.
                    handles.append(handle)
    except FileNotFoundError:
        print(f"Handles file not found at {file_path}. Using empty list.")
    return handles


def start_live_for_handles(handles: List[str], interval: int = 45, max_threads: int = 10):
    """Start live_feed in a daemon thread for up to `max_threads` handles.

    This function returns immediately after threads are started.
    """
    threads = []
    n = min(len(handles), max_threads)
    for i in range(n):
        h = handles[i]
        t = threading.Thread(target=live_feed, args=(h, interval), daemon=True, name=f"live-{h}")
        t.start()
        threads.append(t)
        print(f"Started live feed thread for {h}")
    if not threads:
        print("No handles to start live feeds for.")
    return threads


if __name__ == "__main__":
    # Example usage: set CHANNEL_HANDLE env var or change below
    CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")
    INTERVAL = int(os.getenv("LIVE_INTERVAL", "10"))
    ALL = os.getenv("ALL_HANDLES")
    if ALL and ALL.lower() in ("1", "true", "yes"):
        handles = load_handles()
        print(f"Starting live feeds for {len(handles)} handles (interval={INTERVAL}s).")
        start_live_for_handles(handles, interval=INTERVAL, max_threads=20)
        # main thread waits indefinitely while daemon threads print
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            print("Stopping all live feeds")
    else:
        CHANNEL_HANDLE = CHANNEL_HANDLE or "@GoogleDevelopers"
        print(f"Starting live feed for {CHANNEL_HANDLE} (interval={INTERVAL}s)")
        live_feed(CHANNEL_HANDLE, INTERVAL)
