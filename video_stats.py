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

def batch_list(video_id_list, batch_size):
    for i in range(0, len(video_id_list), batch_size):
        yield video_id_list[i:i + batch_size]


def extract_video_data(video_ids):
    base_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails,snippet,statistics&key={API_KEY}"
    extracted_data = []
    
    try:
        for batch in batch_list(video_ids, 50):
            ids = ",".join(batch)
            url = f"{base_url}&id={ids}"
            
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()

            for item in data.get('items', []):
                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]
                
                video_data = {
                    "video_id": video_id,
                    "title": snippet.get("title"),
                    "publishedAt": snippet.get("publishedAt"),
                    "duration": contentDetails.get("duration"),
                    "viewCount": statistics.get("viewCount"),
                    "likeCount": statistics.get("likeCount"),
                    "commentCount": statistics.get("commentCount"),
                }
                
                extracted_data.append(video_data)

        return extracted_data
    except requests.exceptions.RequestException as e:
        raise e
    
if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    video_data = extract_video_data(video_ids)
    
    