from dataclasses import dataclass


@dataclass
class YoutubeVideoMetadata:
    id: str
    channel_id: str
    viewCount: int
    likeCount: int
    dislikeCount: int
