import dataclasses
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import cache_helper
import sample_data


class RedisMock(dict):

    def get(self, key):
        return super().get(key)

    def set(self, key, value):
        self[key] = value


class TestCache(unittest.TestCase):

    def setUp(self):
        self.patcher = patch("cache_helper.redis_conn", return_value=RedisMock())
        self.mock_redis = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_miss(self):
        func = MagicMock()
        cache_helper.redis_cached(func)("foo")
        func.assert_called_once()

    def test_miss_save(self):
        cache_helper.redis_cached(MagicMock())("foo")
        self.assertIn("foo", self.mock_redis.return_value)

    def test_hit(self):
        video = dataclasses.replace(sample_data.video)
        video.last_update = datetime.utcnow()
        self.mock_redis.return_value.set("foo", video.to_json())
        func = MagicMock()
        cache_helper.redis_cached(func)("foo")
        func.assert_not_called()

    def test_expired_hit(self):
        video = dataclasses.replace(sample_data.video)
        video.last_update = datetime.utcnow() - cache_helper.CACHE_DURATION
        self.mock_redis.return_value.set("foo", video.to_json())
        func = MagicMock()
        cache_helper.redis_cached(func)("foo")
        func.assert_called_once()
