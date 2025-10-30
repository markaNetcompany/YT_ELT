import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLER = "MrBeast"

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
    
if __name__ == "__main__":
    get_playlist_id()