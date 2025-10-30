import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLER = "MrBeast"
MAX_RESULTS = 50

def get_playlist_id():

    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLER}&key={API_KEY}"

        response = requests.get(url)
        
        response.raise_for_status()

        data = response.json()

        channel_items = data["items"][0]

        uploads_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        print(f"Uploads playlist ID: {uploads_playlist_id}")

        return uploads_playlist_id

    except requests.exceptions.RequestException as e:
        raise e

def get_video_ids(playlist_id):
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={MAX_RESULTS}&playlistId={playlist_id}&key={API_KEY}"
    video_ids = []
    pageToken = None
    
    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            for item in data.get('items', []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)
            
            pageToken = data.get("nextPageToken")
            if not pageToken:
                break
        
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
   