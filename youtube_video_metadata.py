from dataclasses import dataclass


@dataclass
class YoutubeVideoMetadata:
    id: str
    channel_id: str
    view_count: int
    like_count: int
    dislike_count: int
