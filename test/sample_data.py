from datetime import datetime, timezone

from model import Video

vm_code_working = "ZMNCLNbUT"
vm_base = "https://vm.tiktok.com/"
www_path_working = "@jeffxchris/video/7096491154841144581"
www_base = "https://www.tiktok.com/"

video = Video(
    title="aaa",
    author="bbb",
    url="https://foo/bar",
    width=123,
    height=456,
)

video_json = """{"title": "aaa", "author": "bbb", "url": "https://foo/bar", "width": 123, "height": 456, "last_update": 0.0}"""

epoch = datetime(1970, 1, 1)
