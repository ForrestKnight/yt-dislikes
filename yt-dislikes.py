# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

from datetime import datetime
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv

from youtube_client_adapter import YoutubeClientAdapter

load_dotenv()

CHANNEL_ID = os.getenv('CHANNEL_ID')
SEARCH_TERMS = os.getenv('SEARCH_TERMS')
API_KEY = os.getenv('API_KEY')

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Video statistics comment template which contains the following info
# views, likes, dislikes, ratio, date
stat_comment = "This is an automated comment to display likes & dislikes for the video you're currently watching, since YouTube decided to disable the dislike count on videos. \nViews: {views}\nLikes: {likes}\nDislikes: {dislikes}\nRatio: {ratio}%\nLast Updated: {date}\nYouTube, please don't ban or shadowban me. I learned how to do this from your own docs. \nLol thanks."

def build_youtube_client(api_service_name, api_version, client_secrets_file) -> YoutubeClientAdapter:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    client = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    return YoutubeClientAdapter(client, API_KEY)

def main():
    client: YoutubeClientAdapter = build_youtube_client("youtube", "v3", "YOUR_CLIENT_SECRET_FILE.json")
    for video in client.get_channel_videos(CHANNEL_ID):
        ratio = 0 if video.likeCount == 0 else round(100 * video.likeCount / (video.likeCount + video.dislikeCount))
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        updated_comment_text = stat_comment.format(views=video.viewCount, likes=video.likeCount, dislikes=video.dislikeCount, ratio=ratio, date=date)
        print(updated_comment_text)
        client.create_or_update_comment(updated_comment_text, video.channel_id, video.id, SEARCH_TERMS)
                
if __name__ == "__main__":
    main()
