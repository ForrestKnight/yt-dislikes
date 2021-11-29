import unittest
from mockito import when, mock, any

from youtube_client_adapter import YoutubeClientAdapter


class TestYoutubeClientAdapter(unittest.TestCase):
    def test_get_channel_videos(self):
        list_search_response = {
            "items": [
                {
                    "id": {
                        "videoId": "testVideoId"
                    }
                }
            ]
        }
        list_videos_response = {
            "items": [
                {
                    "id": "testVideoId",
                    "statistics": {
                        "viewCount": 0,
                        "likeCount": 0,
                        "dislikeCount": 0
                    }
                }
            ]
        }
        client = self.__create_client(list_search_response, list_videos_response, "testApiKey")
        videos = client.get_channel_videos("testChannelId")
        self.assertEqual(len(videos), 1)
        video = videos[0]
        self.assertEqual(video.id, "testVideoId")
        self.assertEqual(video.channel_id, "testChannelId")
        self.assertEqual(video.view_count, 0)
        self.assertEqual(video.like_count, 0)
        self.assertEqual(video.dislike_count, 0)

    def __create_client(self, list_search_response, list_videos_response, api_key: str) -> YoutubeClientAdapter:
        client = mock()

        search = mock()
        when(client).search().thenReturn(search)
        search_list_request = mock()
        when(search).list(part="snippet", channelId=any, type="video", order="date").thenReturn(search_list_request)
        when(search_list_request).execute().thenReturn(list_search_response)

        videos = mock()
        when(client).videos().thenReturn(videos)
        videos_list_request = mock()
        when(videos).list(part="statistics", key=any, id=any).thenReturn(videos_list_request)
        when(videos_list_request).execute().thenReturn(list_videos_response)

        return YoutubeClientAdapter(client, api_key)
    

if __name__ == "__main__":
    unittest.main()