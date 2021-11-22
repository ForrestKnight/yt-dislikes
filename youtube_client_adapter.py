from youtube_video_metadata import YoutubeVideoMetadata

class YoutubeClientAdapter:
    def __init__(self, client, api_key: str) -> None:
        self.client = client
        self.api_key = api_key
    
    def get_channel_videos(self, channel_id: str) -> list[YoutubeVideoMetadata]:
        search_response = self.list_search_results(part="snippet", channelId=channel_id, type="video", order="date")
        video_ids = ",".join([item["id"]["videoId"] for item in search_response["items"]])
        videos_response = self.list_videos(part="statistics", key=self.api_key, id=video_ids) # batch fetch
        videos = [self.__to_video_metadata(item, channel_id) for item in videos_response["items"]]
        print(f"Fetched channel videos: {str([video.__dict__ for video in videos])}")
        return videos

    def create_or_update_comment(self, updated_comment_text: str, channel_id: str, video_id: str, search_terms: str) -> None:
        comments_response = self.list_comment_threads(part="snippet", videoId=video_id, search_terms=search_terms)
        print(f"Comments list response: {str(comments_response)}")
        if comments_response["items"]: # update stat comment
            comment_id = comments_response["items"][0]["id"]
            update_response = self.update_comment(
                part="snippet",
                key=self.api_key,
                body={
                    "id": comment_id,
                    "snippet": { "textOriginal": updated_comment_text }
                }
            )
            print(f"Comment update response: {str(update_response)}")
        else: # create stat comment
            insert_response = self.insert_comment(
                part="snippet",
                key=self.api_key,
                body={
                    "topLevelComment": {
                        "snippet": { "textOriginal": updated_comment_text }
                    },
                    "channelId": channel_id,
                    "videoId": video_id
                }
            ) 
            print(f"Comment insert response {str(insert_response)}")
    
    def insert_comment(self, **kwargs):
        request = self.client.commentThreads().insert(**kwargs)
        return request.execute()
    
    def update_comment(self, **kwargs):
        request = self.client.comments().update(**kwargs)
        return request.execute()
    
    def list_comment_threads(self, **kwargs):
        request = self.client.commentThreads().list(**kwargs)
        return request.execute()
    
    def list_search_results(self, **kwargs):
        request = self.client.search().list(**kwargs)
        return request.execute()
    
    def list_videos(self, **kwargs):
        request = self.client.videos().list(**kwargs)
        return request.execute()
    
    def __to_video_metadata(self, video_response_item, channel_id: str) -> YoutubeVideoMetadata:
        statistics = video_response_item["statistics"]
        return YoutubeVideoMetadata(
            video_response_item["id"],
            channel_id,
            int(statistics["viewCount"]),
            int(statistics["likeCount"]),
            int(statistics["dislikeCount"])
        )
