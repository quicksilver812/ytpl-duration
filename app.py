from flask import Flask, render_template, request, jsonify
from googleapiclient.discovery import build
import os

app = Flask(__name__)

API_KEY = 'API_KEY_HERE'

def get_playlist_duration(playlist_url):
    try:
        playlist_id = playlist_url.split("list=")[1]
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        
        total_seconds = 0
        next_page_token = None
        
        while True:
            playlist_items_request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            playlist_items_response = playlist_items_request.execute()
            
            video_ids = [item['contentDetails']['videoId'] for item in playlist_items_response['items']]
            
            video_details_request = youtube.videos().list(
                part='contentDetails',
                id=','.join(video_ids)
            )
            video_details_response = video_details_request.execute()
            
            for video in video_details_response['items']:
                duration = video['contentDetails']['duration']
                duration_seconds = parse_duration(duration)
                total_seconds += duration_seconds
            
            next_page_token = playlist_items_response.get('nextPageToken')
            if not next_page_token:
                break
        
        total_duration = format_duration(total_seconds)
        return total_duration
    except Exception as e:
        return str(e)

def parse_duration(duration):
    import isodate
    parsed_duration = isodate.parse_duration(duration)
    return int(parsed_duration.total_seconds())

def format_duration(total_seconds):
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours}h {minutes}m {seconds}s'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    playlist_url = data.get('url')
    if not playlist_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    total_duration = get_playlist_duration(playlist_url)
    return jsonify({'total_duration': total_duration})

if __name__ == '__main__':
    app.run(debug=True)
