# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

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
    requestVidId = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
        order="date"
    )
    responseVidId = requestVidId.execute()
 
    for item in responseVidId['items']:

        vidId = item['id']['videoId']

        ### Get statistics
        requestStats = youtube.videos().list(
            part="statistics",
            id=vidId
        )
        responseStats = requestStats.execute()

        # Format & display statistics
        for item in responseStats['items']:
            views = item['statistics']['viewCount']
            likes = item['statistics']['likeCount']
            dislikes = item['statistics']['dislikeCount']
    
        ratio = float(likes) / (float(likes) + float(dislikes)) * 100
        today = date.today()
        currentDate = today.strftime("%b-%d-%Y")

        textOriginal = (
            "This is an automated comment to display likes & dislikes for the video you're currently watching, since YouTube decided to disable the dislike count on videos.\n"
            f"Views: {views}\n"
            f"Likes: {likes}\n"
            f"Dislikes: {dislikes}\n"
            f"Ratio {str(round(ratio, 1))}%\n"
            f"Last Updated {currentDate}\n"
            "YouTube, please don't ban or shadowban me. I learned how to do this from your own docs.\nLol thanks."
        )

        ### Get my stat comment
        requestCommentId = youtube.commentThreads().list(
            part="snippet",
            moderationStatus="published",
            order="time",
            searchTerms=SEARCH_TERMS,
            videoId=vidId
        )
        responseCommentId = requestCommentId.execute()

        ### Create or update stat comment
        if responseCommentId["items"]:
            for item in responseCommentId['items']:
                commentId = item['id']
                # Update existing stat comment
                requestUpdate = youtube.comments().update(
                    part="snippet",
                    body={
                        "id": commentId,
                            "snippet": {
                                "textOriginal": textOriginal
                        }
                    }
                )
                responseUpdate = requestUpdate.execute()
                print(responseUpdate)
        else:
            # Create new stat comment
            requestComment = youtube.commentThreads().insert(
                part="snippet",
                body={
                "snippet": {
                    "topLevelComment": {
                    "snippet": {
                        "textOriginal": textOriginal
                    }
                    },
                    "channelId": CHANNEL_ID,
                    "videoId": vidId
                }
                }
            )
            responseComment = requestComment.execute()
            print(responseComment)
                
if __name__ == "__main__":
    main()
