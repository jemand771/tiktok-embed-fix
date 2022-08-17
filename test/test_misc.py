import dataclasses
import functools
import json
import unittest
from datetime import datetime, timezone

import model
import sample_data
from model import Video


# TODO feels like naive vs. aware datetimes aren't quite working yet
class TestModel(unittest.TestCase):

    def test_serialization(self):
        video = dataclasses.replace(sample_data.video)
        video.last_update = sample_data.epoch
        self.assertEqual(video.to_json(), sample_data.video_json)

    def test_deserialization(self):
        video = dataclasses.replace(sample_data.video)
        video.last_update = sample_data.epoch
        self.assertEqual(Video.from_json(sample_data.video_json), video)

    # this is here just to ensure I don't break json serialization for non-datetime objects
    def test_serializer_fail(self):
        self.assertRaises(TypeError, functools.partial(json.dumps, object(), default=model.serializer))
