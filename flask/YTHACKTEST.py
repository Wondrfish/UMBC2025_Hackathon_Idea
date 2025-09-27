import os
import sys
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# -----------------------------
# CONFIGURATION
# -----------------------------

# API Key for public requests
API_KEY = "AIzaSyBH6eIGSnQymH14UqE6NfO6Wm62PCpG7Us"

# Example public channel ID (GoogleDevelopers)
PUBLIC_CHANNEL_ID = "@GoogleDevelopers"

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def get_youtube_service_api_key():
    """Create a YouTube API service using an API key."""
    return googleapiclient.discovery.build(
        "youtube", "v3", developerKey=API_KEY
    )

# -----------------------------
# API REQUEST FUNCTIONS 
# -----------------------------
def get_public_channel_info():
    """Retrieve info about a public channel using an API key."""
    youtube = get_youtube_service_api_key()
    request = youtube.channels().list(
        part="snippet, statistics",
        forHandle=PUBLIC_CHANNEL_ID
    )
    response = request.execute()

    print(f"{PUBLIC_CHANNEL_ID} Channel Info (API Key):")
    #print(response)
    
    channel = response["items"][0]
   
    channel_name = channel["snippet"]["title"]
    channel_pic = channel["snippet"]["thumbnails"]["default"]["url"]
    stats = channel["statistics"]
    
    # Print or return
    print("Channel Name:", channel_name)
    print("Channel Pic URL:", channel_pic)
    print("Statistics:", stats)

# -----------------------------
# MAIN
# -----------------------------

def main():
        get_public_channel_info()



if __name__ == "__main__":
    main()
