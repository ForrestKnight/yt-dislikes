from dataclasses import dataclass


@dataclass
class YoutubeVideoMetadata:
    id: str
    channel_id: str
    view_count: int
    like_count: int
    dislike_count: int

def to_video_metadata(video_response_item, channel_id: str) -> YoutubeVideoMetadata:
    statistics = video_response_item["statistics"]
    return YoutubeVideoMetadata(
        video_response_item["id"],
        channel_id,
        int(statistics["viewCount"]),
        int(statistics["likeCount"]),
        int(statistics["dislikeCount"])
    )