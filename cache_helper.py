import functools
import os
from datetime import datetime, timedelta

import redis

from model import Video

# TODO make options configurable
CACHE_DURATION = timedelta(hours=1)


@functools.cache
def redis_conn():
    redis_opts = {key: value for key, value in dict(
        host=os.environ.get("REDIS_HOST"),
        port=os.environ.get("REDIS_PORT"),
        db=os.environ.get("REDIS_DB")
    ).items() if value is not None}
    return redis.Redis(**redis_opts)


# TODO this doesn't really have to be a decorator
def redis_cached(func):
    @functools.wraps(func)
    def wrapper(url):
        conn = redis_conn()
        data = conn.get(url)
        if data is not None:
            video = Video.from_json(data)
            if datetime.utcnow() - video.last_update < CACHE_DURATION:
                return video
        video = func(url)
        conn.set(url, video.to_json())
        return video

    return wrapper
