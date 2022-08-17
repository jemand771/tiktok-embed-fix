from yt_dlp import YoutubeDL

import cache_helper
from model import Video


@cache_helper.redis_cached
def extract_info(url):
    with YoutubeDL() as ytdl:
        info = ytdl.extract_info(url, download=False)
        fmt = select_best_format(info["formats"])
        return Video(
            title=info["title"],
            author=f"{info['creator']} (@{info['uploader']}) on TikTok",
            **{key: val for key, val in fmt.items() if key in ("url", "width", "height")}
        )


def select_best_format(formats):
    h264 = [fmt for fmt in formats if fmt["vcodec"] == "h264"]
    all_direct = [fmt for fmt in h264 if fmt["format_note"].startswith("Direct video")]
    direct = [fmt for fmt in all_direct if fmt["format_note"] == "Direct video"]
    if direct:
        return direct[0]
    if all_direct:
        return all_direct[0]
    if h264:
        return h264[0]
    raise Exception("could not find suitable format")
