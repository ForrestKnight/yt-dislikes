# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from datetime import date
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ID = os.getenv('CHANNEL_ID')
SEARCH_TERMS = os.getenv('SEARCH_TERMS')

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    ### Get videoId list
    request_vid_id = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
        order="date"
    )
    response_vid_id = request_vid_id.execute()
 
    for item in response_vid_id['items']:

        vid_id = item['id']['videoId']

        ### Get statistics
        request_stats = youtube.videos().list(
            part="statistics",
            id=vid_id
        )
        response_stats = request_stats.execute()

        # Format & display statistics
        for item in response_stats['items']:
            views = item['statistics']['viewCount']
            likes = item['statistics']['likeCount']
            dislikes = item['statistics']['dislikeCount']
    
        ratio = likes / (likes + dislikes) * 100
        today = date.today()
        currentDate = today.strftime("%b-%d-%Y")

        text_original = "\n".join([
            "This is an automated comment to display likes & dislikes for the video you're currently watching,"
            "since YouTube decided to disable the dislike count on videos.",
            f"Views: {views}",
            f"Likes: {likes}",
            f"Dislikes: {dislikes}",
            f"Ratio: {round(ratio, 1)}%",
            f"Last Updated: {currentDate}",
            "YouTube, please don't ban or shadowban me. I learned how to do this from your own docs.",
            "Lol thanks."
        ])

        ### Get my stat comment
        
        request_comment_id = youtube.commentThreads().list(
            part="snippet",
            moderationStatus="published",
            order="time",
            searchTerms=SEARCH_TERMS,
            videoId=vid_id
        )
        response_comment_id = request_comment_id.execute()

        ### Create or update stat comment
        if response_comment_id["items"]:
            for item in response_comment_id['items']:
                comment_id = item['id']
                # Update existing stat comment
                request_update = youtube.comments().update(
                    part="snippet",
                    body={
                        "id": comment_id,
                            "snippet": {
                                "textOriginal": text_original
                        }
                    }
                )
                response_update = request_update.execute()
                print(response_update)
        else:
            # Create new stat comment
            request_comment = youtube.commentThreads().insert(
                part="snippet",
                body={
                "snippet": {
                    "topLevelComment": {
                    "snippet": {
                        "textOriginal": text_original
                    }
                    },
                    "channelId": CHANNEL_ID,
                    "videoId": vid_id
                }
                }
            )
            response_comment = request_comment.execute()
            print(response_comment)
                
if __name__ == "__main__":
    main()
